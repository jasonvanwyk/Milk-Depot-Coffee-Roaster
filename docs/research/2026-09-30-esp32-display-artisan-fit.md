# ESP32 Integrated-Display Board: Fit for Purpose and Prior Art

Research date: 30 September 2026. Effort: medium (web search plus targeted page reads). Items marked "unverified" could not be confirmed from a source I could read.

## Summary

- Prior art for "ESP32 + thermocouple + Artisan" is plentiful, but almost all of it uses a plain ESP32 DevKit plus a small OLED or 16x2 LCD. No project with a colour-TFT ESP32 board (T-Display-S3, CYD, M5Stack) plus MAX31855 plus Artisan was found.
- Artisan's TC4 serial protocol over USB is a fully supported and simple path. WebSocket over WiFi is the common ESP32 alternative in community projects. Nothing found in Artisan 4.0 to 4.2 changes the TC4 path.
- The biggest technical risk is not the display. It is that the probes are grounded-junction: a bare MAX31855 will not work reliably with them regardless of MCU or board. The per-channel isolation plan is sound and is not made unnecessary by moving to a 3.3V ESP32.
- USB serial: a board with a bridge chip (CP2102/CH340/CH9102) or native USB will both reset or re-enumerate under some conditions. It is manageable with firmware and Artisan settings, but must be bench-tested against Artisan 3.4.0 on the Pi.

## 1. Prior art

| Project | Hardware | Artisan link | Notes |
|---|---|---|---|
| [sakunamary/TC4-WB](https://github.com/sakunamary/TC4-WB) | ESP32, 2x MAX6675, OLED | TC4 protocol over BLE and WiFi-WebSocket (three firmware variants), OTA | BSD-3, 330 commits, actively maintained. Known bug: OLED corrupts on power insertion. Uses MAX6675, not MAX31855. |
| [tyleryoung1230/sr800-artisan](https://github.com/tyleryoung1230/sr800-artisan) | ESP32 DevKit, 1x MAX31855 | TC4 over USB serial, Artisan 4.x | No display. Notes ESP32 bootloader prints garbage at 74880 baud on boot and firmware announces `READY` at 115200. Recommends a USB isolator between PC and ESP for safety. |
| [yamhill/esp32tc4](https://github.com/yamhill/esp32tc4) | ESP32, OLED, MAX6675 | TC4 emulation | Contents not read in detail (unverified beyond search snippet). |
| [ChristianBuechel/Roaster_Control_ESP32](https://github.com/ChristianBuechel/Roaster_Control_ESP32) | ESP32, MCP3424 ADC, TFT over SPI, rotary encoders | Artisan-compatible UART | Only place a TFT appears. Very sparse README (4 commits, 2 stars), no layout details. |
| [gabrielmarcano/esp32-roaster](https://github.com/gabrielmarcano/esp32-roaster) | ESP32 DevKit V1, MAX6675, I2C 16x2 LCD | None (own web dashboard) | Not Artisan. |
| [bitwisetech/popc](https://github.com/bitwisetech/popc) | ESP8266 | Artisan | Popper-mod firmware. Not read in detail. |
| [Coffee4Randy ESP32 page](https://sites.google.com/view/coffee4randy/roaster/esp32) | ESP32 | Artisan | Not read in detail (unverified). |
| [Home-Barista thread on ESP32 TC4](https://www.home-barista.com/roasting/looking-for-esp32-based-artisan-like-sketch-t88914.html) | various | TC4 over USB, BLE | Reports Bluetooth can drop and show blank temperatures momentarily. |

Findings:

- Boards people actually use: generic ESP32 DevKit (DOIT V1 style) with a cheap OLED or 16x2 I2C LCD. Display is treated as secondary because Artisan on the Pi/PC is the main screen.
- Chips: MAX6675 dominates (cheap, no fault types), MAX31855 second. MAX31856 appears in TC4-derived shields ([tc4plus-coffee-roaster-shield](https://github.com/mgerstgrasser/tc4plus-coffee-roaster-shield) referenced in search results, not read in detail).
- Not found: any roaster project using T-Display-S3, CYD (ESP32-2432S028), M5Stack or Waveshare S3 LCD boards with Artisan. This is a search-coverage statement, not proof none exists (unverified). The choice would be relatively unproven for this use.
- What went wrong in projects read: OLED corruption at power-up (TC4-WB); boot garbage on serial (sr800); Bluetooth dropouts (Home-Barista); safety concerns about mains-side grounding.

## 2. Artisan connectivity options

- **USB serial TC4 ("ArduinoTC4")**: Supported natively. Artisan docs confirm the TC4/TC4C protocol at 115200 baud (older firmware used 19200) ([Artisan Arduino page](https://artisan-scope.org/devices/arduino/)). The page does not describe reset behaviour or timeout settings.
- **WebSocket**: Supported as a request/response device. It was introduced for Probat Series III machines ([Discussion 701](https://github.com/artisan-roaster-scope/artisan/discussions/701)). Artisan can send custom commands on an interval or each sample. Limitation: external PIDs are not supported over WebSocket, only TC4, MODBUS and S7 ([Discussion 866](https://github.com/artisan-roaster-scope/artisan/discussions/866)). A community developer found WebSocket easier than Modbus on ESP32.
- **Modbus TCP**: Supported (Artisan v3.1 renewed its Modbus and Bluetooth infrastructure, per the [release notes](https://github.com/artisan-roaster-scope/artisan/releases/tag/v3.1.0)). Standardised but more work on an ESP32. A [ESP8266 + Modbus TCP example](https://github.com/AlexHaijiaZhu/Roaster) exists.
- **Bluetooth**: Used by TC4-WB. One user reports dropouts.
- **Versions after 3.4.0**: Release history shows v4.0.0 (28 January 2026), v4.0.2 (7 February 2026), v4.2.0 (30 June 2026), v4.2.2. Changes noted to TC4-related features are PID-only (2DOF PID, new PID Artisan commands). No serial protocol or WebSocket changes were identified ([ReleaseHistory](https://github.com/artisan-roaster-scope/artisan/blob/master/wiki/ReleaseHistory.md)). The fetch was summarised by a small model, so treat as "no changes found" rather than "confirmed none".
- **Assessment**: For a wired unit next to the Pi, USB serial is the simplest and avoids WiFi pairing, IP address and reconnect logic. WiFi would remove the USB ground path but adds a network dependency in a workshop. Recommend USB serial first, keeping WebSocket as a later option if USB proves troublesome. Note also that USB isolation (see section 4) is another reason a wireless link is attractive.

## 3. USB serial gotchas

- **Auto-reset**: Both external bridge chips and the ESP32-S3 built-in USB-Serial/JTAG can reset the chip on DTR/RTS sequences ([dev.to write-up](https://dev.to/_8729c5bde46be2/why-your-esp32-resets-every-time-you-open-the-serial-monitor-and-how-to-stop-it-5h2l), [esp32.com thread](https://esp32.com/viewtopic.php?t=4988), [arduino-esp32 #8237](https://github.com/espressif/arduino-esp32/issues/8237)). pyserial asserts DTR and RTS on open by default; setting them false after opening is too late, so they must be set before `open()`. Artisan controls its own pyserial calls, so this cannot be changed from the firmware side.
- **Artisan behaviour**: Older Home-Barista threads state Artisan opens and closes the port for every command, resetting Arduinos, and recommend a 10uF capacitor from RESET to GND (remove when uploading), plus a port timeout of 2 seconds or more ([Home-Barista thread](https://www.home-barista.com/roasting/getting-artisan-to-talk-to-arduino-t58234-30.html)). Whether Artisan 3.4.0 still does this per command is unverified; modern versions are reported to keep the port open.
- **ESP32 equivalent of the capacitor**: Adding a capacitor on EN is a known workaround on dev boards, but it interferes with flashing. Better: on a custom board or a board with accessible auto-reset transistors, omit or disable the DTR/RTS reset circuit. This is not possible on most integrated-display boards.
- **Native USB (ESP32-S3)**: Appears as /dev/ttyACM*. Re-enumerates on reset, so the device node can vanish and return; Artisan holds a stale handle. A tinyusb version (0.21.01 and 0.21.02) reset the S3 on host open ([PyDevices issue](https://github.com/PyDevices/usbif/issues/48)), reportedly fixed. `ARDUINO_USB_CDC_ON_BOOT` and `USBMode` settings matter for whether `Serial` is the native CDC port (from Espressif docs, not re-verified here).
- **Bridge chip**: Appears as /dev/ttyUSB*. Port persists across ESP32 resets, so the chip resetting is less disruptive to the host. CP2102 and CH9102 have reliable Linux drivers (in-kernel). CH340 is also in-kernel. Boot ROM output at 74880 baud appears as garbage after each reset (sr800 project), so the firmware should tolerate junk before the first valid line.
- **Recommendation (judgement, not sourced)**: A bridge-chip board (CP2102/CH9102) is the more forgiving choice: the port stays up through resets. If a native-USB S3 board is chosen, test open/close cycles and Artisan reconnect on the Pi before committing. In both cases, have the firmware ignore malformed input and answer `READ` only after boot completes. Poll interval of 1 to 3 seconds for 15 to 20 minutes was not tested by any source found; a bench soak test of 30+ minutes is needed.

## 4. MAX31855 on ESP32 and isolation

### SPI sharing with a display

- On arduino-esp32 core 2.0.x, devices could share a bus with CS arbitration. On core 3.x, changes to SPI GPIO routing reportedly break sharing when the TFT driver takes ownership of the routing ([Adafruit forum thread](https://forums.adafruit.com/viewtopic.php?t=223208), summary from search snippet only, so unverified in detail).
- A working pattern from the [Arduino forum](https://forum.arduino.cc/t/esp32-s3-tft-espi-ili9341-display-and-max31855-thermocouple-ic/1237825): separate `SPIClass` instances for the TFT and the MAX31855, different SCK pins, unique CS pins.
- Practical advice: give the MAX31855 chips their own SPI bus or bit-banged software SPI on free GPIOs, not the display bus. Adafruit_MAX31855 supports software SPI constructors. Read speed needed is trivial (one read per second or less).
- Most integrated-display boards expose limited free GPIOs (the CYD has few usable pins). This is a board-selection constraint.
- Adafruit_MAX31855 behaviour on ESP32/ESP32-S3 specifically: no defect reports found; not tested here (unverified).

### WiFi and readings

No source found linking WiFi transmission to MAX31855 reading errors. One forum thread on a clone module with ESP32, OLED, battery and WiFi exists ([Arduino forum](https://forum.arduino.cc/t/max31855-clone-and-esp32-with-oled-battery-and-wifi/701190)); its details were not read. Power supply quality and probe grounding were the usual causes of noise in sources found. Treat WiFi effect as unverified; keep the MAX31855 supply decoupled and read while WiFi is idle if issues appear.

### Grounded-junction probes

- The MAX31855 fault circuitry grounds T- to detect shorts, so it does not work with a grounded thermocouple. The junction must float ([Adafruit thermocouple guide](https://learn.adafruit.com/thermocouple?view=all), [Adafruit forum](https://forums.adafruit.com/viewtopic.php?t=44725), [datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/max31855.pdf)). The MAX31856 has the same limitation ([Adafruit forum](https://forums.adafruit.com/viewtopic.php?t=115474)), though it adds 50/60Hz filtering and more fault flags. Switching to MAX31856 does not remove the need for isolation.
- Phidgets' guidance for grounded junctions: use an isolated thermocouple interface or a USB isolator ([Phidgets guide](https://www.phidgets.com/docs/Thermocouple_Guide)). Cropster also specifies ungrounded probes for its non-isolated Phidget 1048 ([Cropster help](https://help.cropster.com/en/knowledge/j/k/e/t-type-thermocouples-roasting-intelligence-ri-setup)).

### Is per-channel isolation what comparable projects do?

- Community ESP32/TC4 projects mostly do not isolate; they use ungrounded or insulated probes, or single-channel setups. The sr800 project recommends a USB isolator. The [lygte-info dual thermocouple design](https://lygte-info.dk/project/ThermoSensor%20UK.html) reportedly isolates the SPI bus and supplies with DC-DC converters and chose MAX31856 because SPI is easy to isolate (from a search summary; the page itself could not be fetched, so unverified).
- Per-channel isolation is the professional approach (Phidgets TMP1100 is isolated).

### Does moving to a 3.3V ESP32 make isolation unnecessary?

No, in my assessment (engineering inference, not from a single source):

1. The failure mode is the probe sheath being electrically tied to the roaster frame. MAX31855 T- fault detection and the input differential path do not care about the MCU supply voltage.
2. With several grounded probes on one metal frame, their T- inputs are tied together through the frame. Non-isolated chips sharing one ground and one frame would have those inputs cross-connected, giving fault flags or wrong readings. Per-channel isolation breaks this. A single USB isolator between the ESP32 and the Pi does not fix the cross-channel issue, though it does break the Pi/mains earth loop.
3. Powering from the Pi over USB adds a ground path to mains earth (through the Pi's power supply), so a frame-to-earth potential difference still appears as a ground loop.

### Off-the-shelf isolated options

| Product | Notes | Source |
|---|---|---|
| M5Stack KMeterISO | Single-channel, isolated (CA-IS3641 isolator, STM32F030 onboard), I2C, MAX31855-based | [The Pi Hut listing](https://thepihut.com/products/kmeter-isolation-unit-with-thermocouple-temperature-sensor-max31855) |
| Phidgets TMP1100 | Isolated thermocouple Phidget, USB-attached; channel count, price and Linux/Artisan support not verified | [Phidgets guide](https://www.phidgets.com/docs/Thermocouple_Guide) |
| Phidget 1048 | 4-channel, but ungrounded probes only (per Cropster). Not suitable | Cropster link above |
| Dual MAX31856 boards (Playing With Fusion and others) | Not isolated in the listings seen | search results only |

KMeterISO x3 (I2C, addresses likely need checking, since fixed-address parts may clash: unverified) would avoid a custom isolated board. Cost, ZA availability and address configurability were not checked.

## 5. Display suitability

Limited sourced information found; most of this is general knowledge and flagged accordingly.

- **CYD (ESP32-2432S028)**: 2.8 in 240x320 TN panel (ILI9341 or ST7789 on some revisions) with resistive touch, backlight on GPIO21, about 115 mA at full brightness ([Random Nerd Tutorials](https://randomnerdtutorials.com/cheap-yellow-display-esp32-2432s028r/), [atomic14](https://www.atomic14.com/esp32/boards/esp32-2432s028r/)). TN viewing angle is weak; few free GPIOs. Datasheet operating temperature was not found (unverified).
- **T-Display-S3, Waveshare, M5Stack**: specs not researched in this pass (unverified).
- **AMOLED**: burn-in is a general concern for static layouts (BT/ET/RoR in fixed positions for 15 to 20 minutes daily). Not verified for any specific board; would need pixel shifting or dimming.
- **Heat**: Typical hobby TFT/LCD modules are rated around -20 to +70 C (general knowledge, unverified for the specific boards). Mount the display away from the roaster body and hot exhaust; a 20x4 HD44780 character LCD is commonly rated similarly (about -20 to +70 C for standard grades).
- **Readability at 1 to 2 m**: A 2.8 in screen showing two numbers at large font (about 30 to 40 mm digit height would be readable at 1 to 2 m; the 20x4 LCD has about 5 mm characters, marginal at 2 m). This is estimation, not sourced. Big-number layouts (BT large, ET and RoR secondary) are the sensible pattern. No existing roaster project found documents font sizes or layouts.
- **Lifetime always-on**: LED-backlit TFT lifetime is typically tens of thousands of hours (general knowledge, unverified for these boards). Dim or blank the backlight in idle.

## Risks and mitigations

| Risk | Severity | Mitigation |
|---|---|---|
| Grounded probes fault the MAX31855 or cross-connect channels | High (rules out non-isolated design) | Keep per-channel isolation (isolated DC-DC plus digital isolator), or use ungrounded probes, or off-the-shelf isolated modules (KMeterISO). Bench-test with real probes bolted to the frame. |
| Isolation still needed after switching to ESP32 3.3V | High | See section 4; do not drop isolation because of the MCU change. |
| Board has too few free GPIOs for isolated SPI (3 chips x CS + shared SCK/MISO) | Medium | Check exposed GPIOs before buying. CYD and many integrated boards have very few. Use I2C isolated modules as an alternative. |
| TFT and MAX31855 SPI conflicts on core 3.x | Medium | Separate SPI instance or software SPI for the MAX31855. Pin core version. |
| Native USB CDC re-enumeration or reset when Artisan opens the port | Medium | Prefer a board with a bridge chip. If native USB, soak-test with Artisan 3.4.0. Consider WebSocket fallback. |
| Lost first command after boot or reset | Low to medium | Firmware ignores garbage, answers only complete `READ`, sends nothing unsolicited. Artisan port timeout at 2 s or more. |
| No prior art with colour-TFT boards | Medium | Prototype on a dev kit before committing PCB design. |
| Display heat, glare and burn-in | Low to medium | Mount away from roaster, dim when idle, use non-AMOLED for a static layout. |
| WiFi interference with readings | Low (unverified) | Use USB serial only; leave WiFi off. |
| Artisan 3.4.0 versus 4.x | Low | No TC4 protocol change found. Pi is on Debian packaged 3.4.0; test there. |

## Not verified

- Artisan 3.4.0 serial open/close behaviour per command.
- Specific specs (operating temperature, brightness in nits) for T-Display-S3, Waveshare, M5Stack and CYD panels.
- Adafruit_MAX31855 on ESP32-S3 specifically.
- Phidgets TMP1100 channel count, price, Artisan support; KMeterISO addressing for 3 units and ZA availability.
- Any WiFi-to-thermocouple noise effect.

## Sources

- https://github.com/sakunamary/TC4-WB
- https://github.com/tyleryoung1230/sr800-artisan
- https://github.com/yamhill/esp32tc4
- https://github.com/ChristianBuechel/Roaster_Control_ESP32
- https://github.com/gabrielmarcano/esp32-roaster
- https://github.com/bitwisetech/popc
- https://github.com/mgerstgrasser/tc4plus-coffee-roaster-shield
- https://github.com/AlexHaijiaZhu/Roaster
- https://sites.google.com/view/coffee4randy/roaster/esp32
- https://www.home-barista.com/roasting/looking-for-esp32-based-artisan-like-sketch-t88914.html
- https://www.home-barista.com/roasting/getting-artisan-to-talk-to-arduino-t58234-30.html
- https://artisan-scope.org/devices/arduino/
- https://github.com/artisan-roaster-scope/artisan/blob/master/wiki/ReleaseHistory.md
- https://github.com/artisan-roaster-scope/artisan/releases/tag/v3.1.0
- https://github.com/artisan-roaster-scope/artisan/discussions/701
- https://github.com/artisan-roaster-scope/artisan/discussions/866
- https://dev.to/_8729c5bde46be2/why-your-esp32-resets-every-time-you-open-the-serial-monitor-and-how-to-stop-it-5h2l
- https://esp32.com/viewtopic.php?t=4988
- https://github.com/espressif/arduino-esp32/issues/8237
- https://github.com/PyDevices/usbif/issues/48
- https://forum.arduino.cc/t/esp32-s3-tft-espi-ili9341-display-and-max31855-thermocouple-ic/1237825
- https://forums.adafruit.com/viewtopic.php?t=223208
- https://forum.arduino.cc/t/max31855-clone-and-esp32-with-oled-battery-and-wifi/701190
- https://learn.adafruit.com/thermocouple?view=all
- https://forums.adafruit.com/viewtopic.php?t=44725
- https://forums.adafruit.com/viewtopic.php?t=115474
- https://www.analog.com/media/en/technical-documentation/data-sheets/max31855.pdf
- https://www.phidgets.com/docs/Thermocouple_Guide
- https://help.cropster.com/en/knowledge/j/k/e/t-type-thermocouples-roasting-intelligence-ri-setup
- https://lygte-info.dk/project/ThermoSensor%20UK.html
- https://thepihut.com/products/kmeter-isolation-unit-with-thermocouple-temperature-sensor-max31855
- https://randomnerdtutorials.com/cheap-yellow-display-esp32-2432s028r/
- https://www.atomic14.com/esp32/boards/esp32-2432s028r/
