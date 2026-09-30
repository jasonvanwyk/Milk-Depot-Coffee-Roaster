# ESP32-S3 Native USB: Does Opening the Port Reset the Chip? (Artisan / T-Display-S3)

Researched 30 September 2026. Scope: LilyGO T-Display-S3 (ESP32-S3, native USB, no bridge chip) on a Raspberry Pi 4 (Debian Trixie) running Artisan 3.4.0, device "ArduinoTC4", 115200 baud, `READ` polling every 1 to 3 seconds.

Evidence labels used throughout:

- **[DOC/SRC]** documented by Espressif, or seen directly in source code that was fetched and read for this report
- **[USER]** reported by a user or third party (forum, issue tracker), not independently verified
- **[INFER]** my inference from the above; not directly evidenced

## Summary

| Question | Finding | Confidence |
|----------|---------|------------|
| Can the S3 native USB reset the chip from DTR/RTS? | Yes, by design, in Hardware CDC and JTAG (HWCDC) mode. The USB-Serial/JTAG peripheral decodes RTS/DTR in hardware. | High |
| Does a plain `pyserial` open on Linux trigger it? | Unresolved. No source found either way for the S3 on Linux. Linux `cdc-acm` raises DTR and RTS together in one request, which is not the documented reset pattern (RTS alone), but that is inference only. | Low |
| Does Artisan tolerate a reset on open? | Partly. It sleeps 1 second after open for device 19 (ArduinoTC4) and re-runs its init handshake, but it never closes and reopens the port on errors, so a dead (re-enumerated) port would stay dead until the user toggles OFF/ON. | High (code read) |
| Is there a firmware fix? | Yes for TinyUSB (USB-OTG) CDC mode: plain open cannot reset, and `enableReboot(false)` removes even the bootloader-entry path. No software fix exists for HWCDC mode on the S3. | High (source read) |
| Verdict | Unproven risk with a known, cheap mitigation. Needs one bench test. See the last section. | Medium |

## 1. Does it actually happen?

### 1a. Hardware CDC and JTAG mode (USB-Serial/JTAG controller)

**Reset by DTR/RTS is a designed feature of the peripheral. [DOC/SRC]**

- esptool's docs state that the USB-Serial/JTAG peripheral can only trigger a core reset (it does not re-sample strapping pins) and that the device "disappears from the system" when USB is reconfigured. esptool troubleshooting: https://docs.espressif.com/projects/esptool/en/latest/esp32s3/troubleshooting.html
- esptool's `HardReset` for USB-attached chips is literally `RTS=True`, wait 0.2 s, `RTS=False`, wait 0.2 s. Its comment says chips on the internal USB peripheral "disappear from the bus during reset". (esptool v4.8.1 `esptool/reset.py`, class `HardReset`; current master delegates to `esp_pylib.serial_reset.hard_reset` with the same 0.2 s delays). https://github.com/espressif/esptool/blob/v4.8.1/esptool/reset.py
- esptool's `USBJTAGSerialReset` (enter bootloader) has the comment "Calls inverted to go through (1,1) instead of (0,0)", showing the hardware decodes ordered sequences of (DTR,RTS) states, not just a level. Same file.
- The boot log reason on such a reset is `rst:0x15 (USB_UART_CHIP_RESET)`. Seen on a C3 running a real Artisan-compatible firmware: https://github.com/Dhurzo/LibreRoaster/blob/main/docs/CONNECTION_TYPES.md

**Whether the software can turn it off:**

- The ESP32-C6 register header defines `USB_SERIAL_JTAG_USB_UART_CHIP_RST_DIS` (7 matches when grepped). The ESP32-S3 header `components/soc/esp32s3/register/soc/usb_serial_jtag_reg.h` has **zero** matches for `CHIP_RST`, `RTS` or `DTR` (checked 30 September 2026 on ESP-IDF master). [DOC/SRC] So the S3 does not expose the disable bit that newer chips have. https://github.com/espressif/esp-idf/blob/master/components/soc/esp32s3/register/soc/usb_serial_jtag_reg.h
- arduino-esp32 `HWCDC.cpp` (master, 699c2dc) contains no DTR/RTS handling at all. A user says the same: "HWCDC does not have any code to disable DTR and RTS". [DOC/SRC] plus [USER]: https://forum.arduino.cc/t/problem-with-esp32-c3-rebooting-when-closing-the-serial-port/1217801 and https://github.com/espressif/esp-idf/issues/13075 (closed "Won't Do").

**Does a plain port open trigger it?**

- The Linux `cdc-acm` driver, on port activation, calls `acm_port_dtr_rts(port, true)` which sends `val = USB_CDC_CTRL_DTR | USB_CDC_CTRL_RTS` in a single SET_CONTROL_LINE_STATE request. On close it sends 0. [DOC/SRC] https://github.com/torvalds/linux/blob/master/drivers/usb/class/cdc-acm.c (`acm_port_dtr_rts`, line 676 at master when fetched)
- pyserial asserts DTR and RTS on open by default (its documented default for `dtr`/`rts`). Artisan sets neither (see section 2), so this default applies. [INFER from pyserial docs]
- So the host presents line state (0,0) to (1,1) on open and (1,1) to (0,0) on close. The documented software-reset trigger is RTS=1 with DTR=0 (esptool `HardReset`, and the Arduino TinyUSB path below uses (0,1) as the first step). (1,1) is not that state. **[INFER]** that open does not reset an S3 on Linux, but I found **no source that confirms or refutes it**.
- Conflicting third-party claims, both weak:
  - A dev.to article says both lines low on native-USB boards itself triggers a reset and that `monitor_dtr/rts` should be omitted. [USER, single blog, no evidence shown] https://dev.to/_8729c5bde46be2/why-your-esp32-resets-every-time-you-open-the-serial-monitor-and-how-to-stop-it-5h2l
  - A C3 user reported the reset happens on **close** with third-party software on Windows, and that the same code "does not occur in ESP32-S3 devkit". [USER, C3 and Windows, so weak for this case] https://forum.arduino.cc/t/problem-with-esp32-c3-rebooting-when-closing-the-serial-port/1217801
- Search summaries also repeat "the built-in USB-Serial/JTAG port also resets on DTR/RTS" and that pyserial should set `dtr=False, rts=False` before `open()`. That is a generic recipe; I found no S3-on-Linux report that proves the bug and the fix. [USER]

### 1b. USB-OTG (TinyUSB) CDC mode

Here reset behaviour is **software in arduino-esp32**, and I read it. [DOC/SRC] `cores/esp32/USBCDC.cpp`, master 699c2dc, `USBCDC::_onLineState` (lines ~216-262), `_onLineCoding` (~282-283), `enableReboot` (~324):

```cpp
if (reboot_enable) {
    if (!dtr && rts) { ... lineState = CDC_LINE_1 ...}
    else if (dtr && rts) { if (lineState == CDC_LINE_1) lineState++; ... }
    else if (dtr && !rts) { if (lineState == CDC_LINE_2) lineState++; ... }
    else if (!dtr && !rts) { if (lineState == CDC_LINE_3) usb_persist_restart(RESTART_BOOTLOADER); ... }
}
...
// ArduinoIDE sends LineCoding with 1200bps baud to reset the device
if (reboot_enable && _bit_rate == 1200) usb_persist_restart(RESTART_BOOTLOADER);
```

- A reset needs the exact four-step sequence (0,1) then (1,1) then (1,0) then (0,0), or a 1200 baud line coding. A single (0,0) to (1,1) open does not complete it. The "reset" is `RESTART_BOOTLOADER`, meaning it reboots into download mode, not a normal restart.
- Artisan configures baud 115200 before opening, so the 1200 baud path is not hit. [DOC/SRC on Artisan side; INFER that pyserial sends 115200 first]
- `USBCDC::enableReboot(bool)` sets `reboot_enable`; with `false` both paths are skipped entirely. Docs: https://docs.espressif.com/projects/arduino-esp32/en/latest/api/usb_cdc.html ("enables the device to reboot by the DTR as RTS signals").
- Separate, unrelated bug: espressif/tinyusb 0.21.0~1 and 0.21.0~2 on the S3 reset the chip via an interrupt watchdog when DTR is raised at open (reported on a LilyGO T-Embed, opened 26 September 2026). Not the DTR reset mechanism; it is a TinyUSB DWC2 defect, fixed in MicroPython's tag. [USER] https://github.com/PyDevices/usbif/issues/48 . Check which TinyUSB component version your arduino-esp32 release bundles before relying on TinyUSB mode. [INFER that this matters]

### Arduino-ESP32 2.x versus 3.x

I did not find a documented behavioural change between 2.x and 3.x for the DTR/RTS logic. The `enableReboot` API is present in both docs (the 2.0.14 docs page was among the search results). [DOC] The hardware behaviour in HWCDC mode is set by silicon, not core version. [INFER]

## 2. What does Artisan do when it opens the port?

Source: https://github.com/artisan-roaster-scope/artisan, `src/artisanlib/comm.py`, master at commit `4ca49a3f1de8de4feeceaa0211ca932c4fc8a991` (HEAD on 30 September 2026). Line numbers below are from that file (7,581 lines). [DOC/SRC]

**Port configuration and open** (`confport`, about line 2764; `openport`, line 2745):

```python
def openport(self) -> None:
    ...
        if not self.SP.is_open:
            self.confport()
            #Reinitialize Arduino in case communication was interrupted
            self.SP.open()
            if self.aw.qmc.device == 19:
                libtime.sleep(1) # Arduino takes about 1s after port open until it communicates, as it first restarts
                self.ArduinoIsInitialized = 0  # Assume the Arduino has to be reinitialized
            else:
                libtime.sleep(.1) # avoid possible hickups on startup
```

```python
def confport(self):
    self.SP.port = self.comport; self.SP.baudrate = self.baudrate; self.SP.bytesize = self.bytesize
    self.SP.parity = self.parity; self.SP.stopbits = self.stopbits; self.SP.timeout = self.timeout
    if self.platf != 'Windows':
        self.SP.exclusive = True
```

- No `dsrdtr`, `rtscts`, `setDTR` or `setRTS` anywhere in `comm.py` (grep returned nothing). So pyserial's defaults apply: DTR and RTS asserted on open.
- Default `timeout` is 0.4 s (line 279); the 1 s post-open sleep applies to device 19 only. Device 19 is ArduinoTC4.
- The comment confirms Artisan expects classic Arduinos to auto-restart on open.

**Handshake and read** (`ARDUINOTC4temperature`, line 6966): if the port is not open it opens and sets `ArduinoIsInitialized = 0`. Then, when not initialised, it sends `CHAN;...\n`, sleeps 0.1 s, `readline()`s (0.4 s timeout). It accepts an empty reply or a reply starting with `#`; anything else raises "Arduino could not set channels". If the reply starts with `#`, it goes on to `UNITS;` and `FILT;` (each expects empty or `#`), then sets `ArduinoIsInitialized = 1`. Every poll then does `reset_input_buffer()`, writes `READ\n`, sleeps 0.1 s, `readline()`, and splits on commas.

Consequences for the firmware [INFER from the code]:

- An empty reply to `CHAN` does not error, but leaves `ArduinoIsInitialized = 0`, so Artisan retries the CHAN/UNITS/FILT handshake on the next poll. This is a built-in "no response on first read" recovery.
- `CHAN`, `UNITS` and `FILT` must reply `#` (or nothing). Anything else, including a boot banner arriving in that window, raises an error and that poll returns -1,-1. Junk bytes are flushed by `reset_input_buffer()` before each command, so a banner is only harmful if it arrives after that flush.
- Silence the ESP32 boot log on the USB port (no `Serial.println` banner, and consider disabling the ROM boot print). Note the ROM prints at boot on UART0 or USB-Serial/JTAG unless `DIS_USB_SERIAL_JTAG_ROM_PRINT` is burned. [INFER; the eFuse exists in the S3 table, see section 4]

**Error handling** (line ~7165 onward):

```python
except Exception as e:
    _log.exception(e)
    # self.closeport() # closing the port on error is to serve as the Arduino needs time to restart and has to be reinitialized!
    ...
    return -1.,-1.
```

The `closeport()` on error is **commented out**. So if the ESP32 resets and re-enumerates after Artisan opened the port, the old file descriptor is dead but `SP.is_open` still reads True. Artisan will not reopen automatically, and each poll would return -1. The user would have to press OFF then ON, which closes the port. [INFER from code; not tested]

### Artisan issues and threads

I did not find any Artisan GitHub issue or forum thread about ESP32-S3, native USB or `/dev/ttyACM` resets. Searches: GitHub, home-barista, homeroasters. Absence of results is weak evidence only.

## 3. Reports from people using ESP32 native USB with Artisan

| Project or source | Chip and link | What it says | Evidence |
|-------------------|---------------|--------------|----------|
| LibreRoaster | ESP32-C3, native USB CDC to Artisan | Docs recommend native USB. Boot log shows `rst:0x15 (USB_UART_CHIP_RESET)` on "Verified on real hardware", with Artisan commands answering afterwards. The README's own status table says "Real Artisan Connection: To be tested" and warns hardware integration is not validated. | [USER], self-contradictory. https://github.com/Dhurzo/LibreRoaster |
| LibreRoaster GPIO9 note | Same | On boards with a bridge chip, RTS held during reset can force download mode. Native USB boards boot from flash deterministically. | [USER] https://github.com/Dhurzo/LibreRoaster/blob/main/docs/CONNECTION_TYPES.md |
| sr800-artisan | ESP32 + MAX31855, Artisan TC4 | Recommends a USB isolator. Does not discuss DTR reset. | [USER] https://github.com/tyleryoung1230/sr800-artisan |
| esp32tc4, TC4-WB | ESP32 boards with bridge chips or WiFi | Not native-USB S3 evidence. | https://github.com/yamhill/esp32tc4 , https://github.com/sakunamary/TC4-WB |
| Home-barista thread "Getting Artisan to talk to Arduino" | Classic Arduino | One user could only get data after pressing the hardware reset button, then Artisan initialised fine. Shows the same failure family for classic boards. | [USER] https://www.home-barista.com/roasting/getting-artisan-to-talk-to-arduino-t58234-30.html |

I found **no report of an ESP32-S3 with native USB working or failing with Artisan.** The nearest is the C3 LibreRoaster, which is not proof either way.

## 4. Ways to build around it

### Firmware settings

- `ARDUINO_USB_CDC_ON_BOOT=1` routes `Serial` to native USB. `ARDUINO_USB_MODE=1` selects Hardware CDC and JTAG (HWCDC); `0` selects USB-OTG (TinyUSB). LilyGO documents "USB CDC On Boot: Enabled, USB Mode: CDC and JTAG, Upload Mode: UART0/Hardware CDC" for this board, and notes the board waits for USB access on startup when CDC is enabled. [DOC] https://github.com/Xinyuan-LilyGO/T-Display-S3
- TinyUSB mode: `Serial.enableReboot(false)` (or the `USBSerial` instance). Source-verified above.
- HWCDC mode: no equivalent in arduino-esp32 and no S3 register bit (section 1a).
- eFuses (S3 table, `esp_efuse_table.csv`, checked on master): `DIS_USB_JTAG` (disconnects the JTAG function only; CDC still works), `DIS_USB_SERIAL_JTAG` (disables the whole USB-Serial/JTAG device, which also removes the ROM/HWCDC serial path), `DIS_USB_SERIAL_JTAG_DOWNLOAD_MODE`, `DIS_USB_SERIAL_JTAG_ROM_PRINT`. [DOC/SRC] eFuses are one-time programmable. None is documented as "disable DTR/RTS reset only". A C3 user who tried `DIS_USB_SERIAL_JTAG_DOWNLOAD_MODE` and others reported still rebooting and losing upload capability. [USER] https://github.com/espressif/esp-idf/issues/13075 . Burning `DIS_USB_SERIAL_JTAG` while using TinyUSB (the USB-OTG core) is the documented way to free the pins, but I did not verify it on the S3 with Arduino. [INFER]

### Tolerating the reset

- Timing to first response: not measured. ROM plus second-stage boot on an S3 is a few hundred milliseconds and USB enumeration on Linux adds more; I have no source with numbers. Artisan waits 1.0 s after open, then CHAN with a 0.4 s timeout, so a reset on open plausibly lands the first CHAN on a not-yet-enumerated device. [INFER, unmeasured]
- If the port re-enumerates while Artisan holds it open: the old node disappears and Artisan does not reopen (section 2). A newly enumerated node is often the same `ttyACM0` name but a new device instance, so the old fd stays dead. [INFER]. esptool itself needs a retry-on-disconnect loop that reopens the port up to three times because "targets with internal USB peripherals can drop and re-enumerate the serial device during a reset". [DOC/SRC] esptool `reset.py` (`ResetStrategy` docstring, master).
- Reasonable tolerance design: make the first successful port open the only reset, and have firmware come up fast with no boot-time prints.

### Hardware alternatives

- Use UART0 (GPIO43 TX, GPIO44 RX; LilyGO says these carry serial output when USB CDC is disabled [DOC]) with an external CP2102/FT232-class adapter or the Pi's GPIO UART. Then Artisan's DTR/RTS toggling drives nothing (leave DTR/RTS unconnected on the adapter). Whether the T-Display-S3 breaks out GPIO43/44 to its header needs the pinout/schematic; the LilyGO page did not say. [UNVERIFIED]
- Stable name: a udev rule matching the adapter's `ID_VENDOR_ID`/`ID_MODEL_ID`/`ID_SERIAL_SHORT` (a CP2102/FT232 exposes a serial number; the ESP32-S3 native USB uses Espressif VID 0x303A with a MAC-based serial). Standard udev practice; not researched for this report. [INFER]
- Pi GPIO UART needs 3.3 V logic (same as the S3), so no level shifting is needed. [INFER]

### Non-USB

Artisan can also talk to TC4-style ESP32 firmware over WiFi WebSocket (see TC4-WB above), which avoids the USB question entirely at the cost of a network dependency. Not evaluated further.

### Workaround table

| Method | Evidence level | Downside |
|--------|----------------|----------|
| Switch to USB-OTG (TinyUSB) CDC mode and call `Serial.enableReboot(false)` | Source read (USBCDC.cpp master 699c2dc); works on the ESP32-S3 hardware path used by T-Display-S3 [DOC/SRC] | Reflashing needs BOOT+RST held by hand once reboot is disabled; TinyUSB version regression (espressif/tinyusb 0.21.0~1/~2 reset on open) must be avoided [USER]; need to test enumeration and `while(!Serial)` behaviour |
| Same, but leave `enableReboot(true)` (default) | Source read: only a four-state sequence or 1200 baud triggers bootloader entry; Artisan does neither [DOC/SRC + INFER] | Slight risk of an accidental bootloader entry from other host software |
| Stay in HWCDC mode, rely on Linux open behaviour | Reasoning only: Linux raises DTR+RTS together, not RTS alone [INFER] | Unverified; no software fix if it does reset; no S3 disable bit |
| Host-side: open with `dtr=False, rts=False` before `open()` | Widely recommended in [USER] posts | Artisan does not expose this; would need a patch to `comm.py` or a wrapper (a tiny pty/serial proxy). Not supported upstream |
| Host-side: `stty -F /dev/ttyACM0 -hupcl` before Artisan starts | Suggested in [USER] search results for Linux | Avoids the drop on close, not necessarily the raise on open; a device that re-enumerates loses the setting |
| Burn `DIS_USB_SERIAL_JTAG` eFuse | eFuse exists in S3 table [DOC/SRC] | Permanent; loses the built-in USB serial/JTAG path; not proven to leave a working Arduino CDC path; blocks easy reflashing; not needed unless TinyUSB mode is used |
| UART0 via external USB-serial adapter or Pi GPIO UART | Standard practice; C3 case "bridge chip" behaviour is well documented [USER] | Needs pin access, extra hardware, udev rule; a bridge chip's own DTR/RTS must be left unwired to avoid the classic auto-reset |
| Artisan WebSocket over WiFi | Existing project (TC4-WB) | Network dependency; separate firmware work |

## 5. Verdict

**Status: unproven risk, cheaply mitigable. Not a confirmed defect.**

- **Documented and certain:** the S3's USB-Serial/JTAG peripheral can reset the chip from the host's DTR/RTS lines, and this cannot be disabled in software on the S3. In TinyUSB mode the only such paths are a specific four-step DTR/RTS sequence or 1200 baud, and both can be disabled.
- **Not proven:** that a plain Linux `pyserial` open (what Artisan does) produces the resetting pattern in HWCDC mode. The evidence points to "probably not" (single (0,0) to (1,1) request), but the only third-party statements either way are weak.
- **Artisan-specific risk is real if it does reset:** Artisan waits 1 s after open, has a self-retrying handshake, but never reopens a dead port. So a reset during open would leave the session dead until OFF/ON.
- **Confidence:** medium that this is a minor nuisance with a known fix; low on the exact HWCDC-on-Linux behaviour.

**Recommendation:** build the firmware with TinyUSB CDC and `enableReboot(false)`, keep the boot quiet, and make `CHAN`/`UNITS`/`FILT` reply `#`. Fallback if TinyUSB proves troublesome: UART0 through an external adapter.

### Still unverified: needs a bench test

1. On the Pi (Debian Trixie), with the T-Display-S3 in HWCDC mode running a counter, open the port with `python3 -c "import serial; s=serial.Serial('/dev/ttyACM0',115200); ..."` and watch `dmesg -w` for a USB disconnect/reconnect and the uptime counter resetting. Repeat with Artisan's ON button.
2. Repeat in TinyUSB mode (`enableReboot(false)`) and confirm no reset and stable enumeration.
3. Measure time from open to first valid `READ` reply, against Artisan's 1.0 s sleep plus 0.4 s timeout.
4. If Artisan ever sees a reset, confirm whether it recovers without OFF/ON (predicted: it does not).
5. Check which `espressif/tinyusb` version the installed arduino-esp32 core bundles (avoid 0.21.0~1 and ~2).
6. Confirm whether GPIO43/44 are on the T-Display-S3 header.

## Sources

- Artisan `comm.py`: https://github.com/artisan-roaster-scope/artisan/blob/master/src/artisanlib/comm.py (commit 4ca49a3f1de8de4feeceaa0211ca932c4fc8a991 at time of reading)
- arduino-esp32 `USBCDC.cpp`: https://github.com/espressif/arduino-esp32/blob/master/cores/esp32/USBCDC.cpp (master 699c2dcf50f1b7bd0d3e269ff43f016b087cf801)
- arduino-esp32 `HWCDC.cpp`: https://github.com/espressif/arduino-esp32/blob/master/cores/esp32/HWCDC.cpp
- Arduino-ESP32 USB CDC API docs: https://docs.espressif.com/projects/arduino-esp32/en/latest/api/usb_cdc.html
- ESP-IDF S3 USB-Serial/JTAG register header: https://github.com/espressif/esp-idf/blob/master/components/soc/esp32s3/register/soc/usb_serial_jtag_reg.h
- ESP-IDF S3 eFuse table: https://github.com/espressif/esp-idf/blob/master/components/efuse/esp32s3/esp_efuse_table.csv
- esptool `reset.py` v4.8.1: https://github.com/espressif/esptool/blob/v4.8.1/esptool/reset.py
- esptool troubleshooting (S3): https://docs.espressif.com/projects/esptool/en/latest/esp32s3/troubleshooting.html
- esptool boot mode selection (S3): https://docs.espressif.com/projects/esptool/en/latest/esp32s3/advanced-topics/boot-mode-selection.html
- ESP-IDF USB-Serial/JTAG console guide (no DTR/RTS detail): https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-guides/usb-serial-jtag-console.html
- Linux `cdc-acm.c`: https://github.com/torvalds/linux/blob/master/drivers/usb/class/cdc-acm.c
- esp-idf issue 13075 (C3 reboot on close, Won't Do): https://github.com/espressif/esp-idf/issues/13075
- Arduino forum, C3 reboot on close: https://forum.arduino.cc/t/problem-with-esp32-c3-rebooting-when-closing-the-serial-port/1217801
- esp-idf issue 14040 (`--no-reset` still resets S3): https://github.com/espressif/esp-idf/issues/14040
- esp-idf issue 15597 (S3 port disappears after reset): https://github.com/espressif/esp-idf/issues/15597
- esp-idf issue 13946 (permanently disabling USB-JTAG on S3): https://github.com/espressif/esp-idf/issues/13946
- PyDevices/usbif issue 48 (TinyUSB 0.21.0~1/~2 reset on open): https://github.com/PyDevices/usbif/issues/48
- dev.to article on serial-monitor resets: https://dev.to/_8729c5bde46be2/why-your-esp32-resets-every-time-you-open-the-serial-monitor-and-how-to-stop-it-5h2l
- LibreRoaster (C3, Artisan, native USB CDC): https://github.com/Dhurzo/LibreRoaster and https://github.com/Dhurzo/LibreRoaster/blob/main/docs/CONNECTION_TYPES.md
- sr800-artisan: https://github.com/tyleryoung1230/sr800-artisan
- esp32tc4: https://github.com/yamhill/esp32tc4
- TC4-WB: https://github.com/sakunamary/TC4-WB
- Home-barista thread: https://www.home-barista.com/roasting/getting-artisan-to-talk-to-arduino-t58234-30.html
- LilyGO T-Display-S3 repo (board settings): https://github.com/Xinyuan-LilyGO/T-Display-S3

Notes on source quality: esp32.com forum pages (topics 22532, 43163) returned bot-challenge pages and could not be read; statements from them in this report appear only through search-result summaries and are not relied on. Several GitHub issue pages were read through a summarising fetch tool, not in full.
