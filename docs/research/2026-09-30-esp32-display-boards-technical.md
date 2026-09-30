# ESP32 Boards With Built-In Display: Technical Comparison

Date: 30 September 2026
Purpose: Decide whether an ESP32 board with an integrated display beats a bare ESP32-WROOM-32E module plus a separate Keyestudio MD0074 20x4 LCD for the Milk Depot roaster monitor.

## Requirements Used (as corrected)

- 3 thermocouple channels (possibly only 2). Each is a galvanically isolated MAX31855 breakout powered from 5V. Host-side logic can be 3.3V.
- GPIO needed: SCK, MISO, CS1, CS2, CS3 = 5 usable pins (4 for two channels), plus 1 for a mode button if the board has no onboard user button. MISO may be input-only.
- 5V (USB VBUS) pin able to supply roughly 300 mA to the external breakouts.
- USB serial to a Raspberry Pi 4 running Artisan (TC4 protocol, 115200 baud, port opened by the host app).
- Warm ambient (40-50 C), bright workshop lighting, enclosure near a hot gas roaster.

Verdict labels: PASS-3 = 5 usable GPIO + 5V pin available for 3 channels; PASS-2 = only 2 channels; FAIL = cannot practically do 2 channels without hardware hacks.

Evidence caveat: many vendor pages do not publish operating temperature, brightness or 3.3V regulator current. Those are marked "unverified" and should not be read as "fine". Board-level pin claims come from vendor docs or community pinouts; nothing was tested on hardware.

## Comparison Table

| Board | MCU / flash / PSRAM | Display | Free GPIO for SCK/MISO/CS x3 | 5V pin | USB / serial | Published temp range | Approx USD | GPIO verdict |
|---|---|---|---|---|---|---|---|---|
| LilyGO T-Display-S3 (non-touch) | ESP32-S3R8, 16 MB, 8 MB OPI | 1.9 in IPS TFT, 170x320, ST7789V, 8-bit parallel, no touch, nits unpublished | 6 clean header GPIOs (1, 2, 16, 17, 18, 21) plus GPIO10-13 (SPI-labelled) and 43/44 (UART) on 2.54 mm headers | Yes, on header P2 | Native USB-C (S3 USB) | Unverified | 23-26 (LilyGO lists 9.04 for bare board without headers) | PASS-3 |
| LilyGO T-Display-S3 Touch | Same | Same + capacitive touch | Touch uses GPIO16/17/18/21, leaving 1, 2, 10-13, 43/44 | Yes | Native USB-C | Unverified | 37-39 | PASS-3 (fewer clean pins) |
| LilyGO T-Display-S3 AMOLED / AMOLED Plus | ESP32-S3R8, 16 MB, 8 MB OPI | 1.91 in AMOLED, 536x240, RM67162 QSPI, optional touch, nits unpublished (unverified) | "More GPIO than T-Display-S3" per wiki; exact list unverified | Unverified | USB-C native | Unverified | 32-34 | Unverified (probably PASS-3) |
| LilyGO TTGO T-Display (original ESP32) | ESP32, 4 MB flash | 1.14 in IPS, 135x240, ST7789 | Header exposes many GPIOs (2, 12, 13, 15, 17, 25, 26, 27, 32, 33, 36-39 from memory, unverified) | Yes (unverified) | USB-serial bridge chip (model varies by revision, unverified) | Unverified | about 12-20 (unverified) | PASS-3 likely (unverified) |
| Adafruit ESP32-S3 Reverse TFT Feather | ESP32-S3, 4 MB flash, 2 MB PSRAM | 1.14 in IPS TFT, 240x135, ST7789, on the reverse side, no touch | A0-A5, D5, D6, D9-D13, SCK, MOSI, MISO, RX, TX all on Feather headers; ample | Yes, "USB" pin (VBUS); 3.3V regulator 500 mA peak | Native USB-C | Not published on product page | 24.95 | PASS-3, best pin story |
| Heltec WiFi Kit 32 (V3) | ESP32-S3FN8, 8 MB | 0.96 in OLED, 128x64 | Dual 18-pin headers; 2 SPI, 2 I2C, 3 UART; enough GPIO | Likely (unverified) | CP2102 bridge, USB-C | -20 to 70 C (board) | 12.99 | PASS-3 (display very small) |
| Heltec WiFi Kit 32 (V2 / older) | ESP32 | 0.96 in OLED | Not checked | Not checked | CP2102, micro-USB | Not checked | Not checked | Unverified (superseded by V3) |
| ESP32-2432S028R "CYD" 2.8 in | ESP32-WROOM-32, 4 MB | 2.8 in TFT, 240x320, ILI9341 (some batches ST7789), resistive XPT2046, no nits published | Only IO35 (input-only), IO22, IO27, plus IO21 (backlight). IO16/17/4 are RGB LED; SD pins IO5/18/19/23 free only if SD unused | Yes: P1 VIN 5V | CH340; Micro-USB and/or USB-C by revision | Unverified | about 10-15 | FAIL (1 clean channel; 3 needs pin hacks) |
| Sunton ESP32-3248S035 / 8048S043 / 8048S050 / 8048S070 (3.5-7 in) | ESP32 or ESP32-S3, PSRAM on RGB models | 3.5 in SPI or 4.3-7 in 16-bit RGB IPS/TN, touch | RGB bus consumes nearly all GPIO; roughly 2 free pins on 7 in; I2C/UART on JST 1.28 mm connectors | Unverified | Bridge (revision dependent) | Unverified | about 20-45 | FAIL |
| Elecrow CrowPanel 2.8 in HMI (ESP32) | ESP32-WROOM-32-N4 | 2.8 in TFT, 240x320, ILI9341V, resistive | GPIO port IO25, IO32; UART IO16/17; I2C IO21/22. Six pins if UART and I2C connectors are repurposed | Unverified | USB-C, bridge chip unverified | Not published on page | about 20-30 (unverified) | PASS-3 only by repurposing connectors (unverified) |
| Elecrow CrowPanel 5.0 in HMI | ESP32-S3-WROOM-1-N4R8 | 5.0 in TN (not IPS), 800x480 RGB, GT911 touch | 2 GPIO, 2 UART, 2 I2C on connectors | External 5 V 2 A adapter recommended | USB chip unverified | -20 to 70 C | about 40-60 (unverified) | FAIL to PASS-2 by repurposing (unverified) |
| Elecrow CrowPanel 2.4 / 3.5 / 4.3 / 7.0 (and Advanced S3/P4 lines) | Various | Various | Not checked in detail | Not checked | Not checked | 7 in P4: -20 to 70 C | Varies | Unverified |
| Waveshare ESP32-S3-Touch-LCD-4.3 (and 4.3B, 5, 7 in) | ESP32-S3, 16 MB, 8 MB PSRAM | 4.3 in IPS, 800x480 RGB, 270 nits, 160 deg viewing, cap. touch | RGB display uses about 20 GPIO; PH2.0 connectors give I2C (8/9, shared with touch), RS485 (15/16), CAN (19/20, shared with USB), ADC; CH422G expander for backlight, SD CS | 5 V input (450 mA typical) | Native S3 USB-C plus separate CH343P UART USB-C | 0 to 65 C (4.3 and 7 in) | about 40-55 | FAIL |
| Waveshare ESP32-S3-Touch-LCD-3.5 / 3.5B | ESP32-S3R8, 16 MB, 8 MB PSRAM | 3.5 in IPS, 320x480, ST7796, FT6336 touch | "2.54 mm GPIO header"; pin list not verified | Unverified | USB-C (type unverified) | Unverified | about 30-45 (unverified) | Unverified |
| Waveshare ESP32-S3-Touch-LCD-2.8 | ESP32-S3 | 2.8 in IPS, 240x320, ST7789, CST328 touch | 12-pin connector: TXD (GPIO43), RXD (GPIO44), IO18, IO15, VBUS 5V, others unverified | Yes, VBUS on 12-pin connector | Native USB-C ("USB CDC On Boot" needed for Serial) | Not published | about 20-30 (unverified) | PASS-2 (4 pins; 3rd channel unverified) |
| Waveshare ESP32-C6-Touch-LCD-2.8 | ESP32-C6, 16 MB | 2.8 in IPS, 240x320 | Not checked | Not checked | Type-C | Not checked | Not checked | Unverified |
| M5Stack Basic v2.7 | ESP32-D0WDQ6-V3, 16 MB | 2.0 in IPS, 320x240, ILI9342C, 853 nits, no touch | M-Bus exposes G35, G36, G23, G25, G19, G26, G18, G3, G1, G16, G17, G2, G5, G12, G13, G15, G0, G34; three buttons onboard | Yes, on M-Bus | CH9102F bridge, USB-C | Not published | about 30-40 (unverified) | PASS-3 (M-Bus is not a friendly header; needs base/proto module) |
| M5Stack Core2 v1.1 (v1.3 replaces it) | ESP32-D0WDQ6-V3, 16 MB | 2.0 in IPS, 320x240, capacitive touch | Fewer free pins; M-Bus, one Grove port | Yes (M-Bus) | CH9102F | 0 to 60 C | 46.90 (EOL) | Unverified for 5 pins |
| M5Stack CoreS3 / CoreS3 SE | ESP32-S3, 16 MB, 8 MB PSRAM | 2.0 in IPS, 320x240, ILI9342C, touch | Ports A/B/C (HY2.0-4P) plus M-Bus; count of free pins unverified | Yes, via M-Bus / port 5V | Native USB-C (OTG + CDC) | Not published | about 55-60 (unverified) | Unverified (probably PASS-2 or less) |
| M5Stack Tough | ESP32 | 2.0 in IPS, 320x240, cap. touch, 853 nits | Ports A-D (HY2.0-4P): G32, G33, G26, G36, G14, G13, G27, G19, G2, G0, G34 | 5 V USB, or 6-24 V in via RS485 port with DC-DC | CH9102 | Not published | about 55-60 (unverified) | PASS-3 via Grove ports (needs breakout cables) |
| M5StickC Plus2 | ESP32-PICO-V3-02 | 1.14 in TFT, 135x240, ST7789V2 | G0, G25/G26, G36, G32, G33 (5 pins) | Unverified | USB-C (bridge unverified) | 0 to 40 C | about 20 | GPIO-marginal; EOL; temperature fails |
| M5Stack Dial | ESP32-S3 | 1.28 in round | Not checked | Not checked | Not checked | Not checked | Not checked | Unverified; round display unsuited |

Newer boards seen but not evaluated in detail: Waveshare ESP32-S3-Touch-LCD-3.49 (640x172 wide IPS), ESP32-C6 1.8 in AMOLED touch board (December 2025 announcement), Waveshare and Elecrow ESP32-P4 7 in panels. All are touch-first products with dense GPIO use; none were checked for 5-pin availability.

## Per-Board Notes

### LilyGO T-Display-S3 (non-touch)

- Display: 1.9 in ST7789V IPS, 170x320, 8-bit parallel. Small but larger than the 1.14 in class; 320x170 landscape fits BT, ET and rate-of-rise as large numerals.
- GPIO: 13 GPIO on 2.54 mm headers (P1/P2); one source counts 6 clean pins (1, 2, 16, 17, 18, 21) plus 3 (boot/JTAG), 10-13 (SPI-labelled) and 43/44 (UART). That satisfies SCK, MISO, CS1-CS3 with spare. Boot (GPIO0) and IO14 buttons are onboard, so the mode button needs no external pin.
- 5V on header P2. Whether the pin passes current through a diode or connects straight to VBUS is unverified; 300 mA draw must be checked against the schematic.
- Native USB-C only (no bridge). See USB section below.
- Optional 700 mAh battery shell variants exist (K204-01, K206-01). Avoid battery versions near the roaster.
- Size 60.8 x 25.5 mm. No mounting holes reported; cases exist (unverified list). Not designed for panel mounting.
- Libraries: TFT_eSPI (LilyGO fork/config), Arduino_GFX, LovyanGFX, LVGL examples from LilyGO; CircuitPython supported. Maturity: high, widely used since 2022-2023.
- Price about 23-26 USD (ProtoSupplies 24.95-25.95; espboards 23; LilyGO 9.04 for pin-less bare board).
- Operating temperature and brightness: unverified (not on LilyGO page).
- Sources: <https://lilygo.cc/products/t-display-s3>, <https://www.espboards.dev/esp32/lilygo-t-display-s3/>, <https://protosupplies.com/product/lilygo-t-display-s3/>

### LilyGO T-Display-S3 Touch

- Same board with capacitive touch. Touch consumes GPIO16, 17, 18, 21, leaving fewer free pins but still enough (1, 2, 10-13, 43/44). Price 37-39 USD. Touch is unnecessary and adds cost.
- Source: <https://protosupplies.com/product/lilygo-t-display-s3-touch/>

### LilyGO T-Display-S3 AMOLED / AMOLED Plus

- 1.91 in AMOLED, 536x240, RM67162, QSPI. Optional touch. 16 MB flash, 8 MB OPI PSRAM. Two programmable buttons. Active current 90-230 mA with WiFi.
- AMOLED brightness not published on pages checked (unverified). Static high-contrast readouts risk burn-in over a long service life; poor fit for a permanent gauge.
- Price about 32-34 USD.
- Sources: <https://wiki.lilygo.cc/products/t-display-series/t-display-s3-amoled/>, <https://lilygo.cc/en-us/products/t-display-s3-amoled>, <https://www.tindie.com/products/lilygo/lilygo-t-display-s3-esp32-s3-with-191inch-amoled/>

### LilyGO TTGO T-Display (original ESP32)

- Not successfully fetched; the espboards page returned 404. Details in the table are from memory and unverified: 1.14 in 135x240 ST7789, header GPIOs, buttons on GPIO0 and GPIO35, USB-serial bridge (chip differs by revision). Included as a possible cheap fallback and because a dedicated bridge chip avoids native-CDC quirks. Verify before selecting.

### Adafruit ESP32-S3 Reverse TFT Feather

- ESP32-S3, 4 MB flash, 2 MB PSRAM, 1.14 in 240x135 ST7789 IPS TFT on the back of the board (good for panel mounting), three user buttons (D0, D1, D2), STEMMA QT with switchable power, MAX17048 fuel gauge, LiPo charger.
- Pins: A0-A5, D5, D6, D9-D13, SCK, MOSI, MISO, RX, TX free on standard Feather headers. GPIO numbers for the TFT and buttons were not extracted, but the pin set listed is more than sufficient.
- Power: "USB" pin gives VBUS; 3.3V regulator 500 mA peak. 300 mA from the USB pin is limited by the USB host (500 mA per USB 2.0 port; the Pi 4's total USB budget is commonly quoted as 1.2 A, unverified here) and by the board's USB pin trace; fine for three small breakouts but confirm the breakouts' actual draw.
- Native USB-C. Adafruit supports Arduino and CircuitPython officially; a w.FL antenna variant (product 6303) exists.
- Price 24.95 USD. Adafruit product lines are long-lived and documented; strong longevity.
- Operating temperature not published on the pages checked (unverified). The 1.14 in display is the smallest usable; BT/ET/RoR as large digits works, but no four-line text.
- Sources: <https://www.adafruit.com/product/5691>, <https://learn.adafruit.com/esp32-s3-reverse-tft-feather/pinouts>, <https://learn.adafruit.com/esp32-s3-reverse-tft-feather/overview>

### Heltec WiFi Kit 32 (V3)

- ESP32-S3FN8, 8 MB SiP flash, 0.96 in 128x64 OLED, CP2102 bridge with USB-C, LiPo management. Two 18-pin headers with 2 SPI, 2 I2C, 3 UART. Published operating temperature -20 to 70 C. Size 50.2 x 25.5 x 10.2 mm. Price 12.99 USD.
- OLED 0.96 in is too small and dim for a bright workshop; heat and burn-in on small OLEDs unverified. Regulator current not published.
- The CP2102 bridge means the port behaves like a classic UART adapter, avoiding native-CDC reset behaviour.
- Sources: <https://heltec.org/project/wifi-kit32-v3/>, <https://www.espboards.dev/esp32/heltec-wifi-kit-32-v3/>

### ESP32-2432S028R "Cheap Yellow Display" (2.8 in)

- Display: ILI9341 240x320 with resistive XPT2046 touch (later batches may ship ST7789). CH340 bridge. Onboard RGB LED, speaker amp, LDR, microSD.
- Free GPIO: IO35 (input-only, no pull-up), IO22, IO27; IO21 doubles as the backlight. P3 gives IO35/IO22/IO21; CN1 gives IO22/IO27/3V3. IO16/17/4 drive the RGB LED (usable if you lose the LED); SD pins IO5/18/19/23 are free if SD is unused but only reachable at the SD slot.
- For SCK, MISO, CS1-3: SCK = IO22, MISO = IO35 (input is fine), CS1 = IO27, then CS2/CS3 need IO21 (backlight) or the LED/SD pins. Fails the clean 3-channel requirement and only barely does 2. 5V is available on P1 (VIN) alongside serial lines.
- Board size 86 x 50 mm. Price about 10-15 USD. Operating temperature unverified. Many revision/panel variants and clones; low documentation consistency.
- Sources: <https://randomnerdtutorials.com/esp32-cheap-yellow-display-cyd-pinout-esp32-2432s028r/>, <https://github.com/witnessmenow/ESP32-Cheap-Yellow-Display/blob/main/PINS.md>, <https://www.espboards.dev/esp32/cyd-esp32-2432s028/>

### Sunton larger CYD siblings (3.5, 4.3, 5, 7 in)

- The RGB bus consumes nearly all GPIOs. The 7 in board has roughly 2 free GPIO after display, touch and SD; sensors are expected on I2C via a JST 1.28 mm connector. Board revisions (v1.1 versus v1.3) need different init code and published 4.3 in pinouts do not match the 7 in. The 4827S043 is a TN panel with narrow viewing angle.
- Not suited: no 5 free pins.
- Sources: <https://www.atomic14.com/esp32/boards/sunton-esp32-8048s070/>, <https://www.openhasp.com/0.7.0/hardware/sunton/esp32-8048s0xx/>

### Elecrow CrowPanel (2.8 in and 5.0 in checked)

- 2.8 in: ESP32-WROOM-32-N4, ILI9341V 240x320, resistive, TF slot, UART (IO16/17), I2C (IO21/22), GPIO (IO25, IO32), speaker, battery connector, USB-C. Operating temperature not published on the wiki page.
- 5.0 in: ESP32-S3-WROOM-1-N4R8, 800x480 TN panel, GT911 touch, 2 GPIO, 2 UART, 2 I2C, boot/reset buttons; published -20 to 70 C; needs DC 5 V 2 A. Three hardware revisions exist (V3.0 current).
- To reach 5 pins, UART/I2C connector pins must be repurposed as GPIO. Feasible in principle but unverified (pull-ups on the I2C lines would corrupt SPI use, for instance).
- Sources: <https://www.elecrow.com/wiki/esp32-display-282727-intelligent-touch-screen-wi-fi26ble-240320-hmi-display.html>, <https://github.com/Elecrow-RD/CrowPanel-5.0-HMI-ESP32-Display-800x480>, <https://www.makerguides.com/elecrow-2-8-esp32-display-setup-guide/>

### Waveshare ESP32-S3-Touch-LCD-4.3 family (4.3, 4.3B, 5, 7 in)

- ESP32-S3, 16 MB flash, 8 MB PSRAM, 800x480 IPS RGB, 270 nits, 160 degree viewing angle, 5-point capacitive touch. Operating temperature 0 to 65 C (published for 4.3 and 7 in). Typical draw 5 V 450 mA. Dimensions 106.1 x 67.8 mm (touch version).
- Pin use: RGB display takes about 20 GPIO; touch GPIO4/8/9; RS485 on GPIO15/16; CAN on GPIO19/20 (shared with native USB, selected by CH422G EXIO5); TF card GPIO11-13 with CS through the expander. Headers are PH2.0 with I2C, RS485, CAN and ADC only. No 5 free GPIO.
- Has both native USB and a CH343P UART port, which is convenient.
- 0-65 C is a tight fit against a 40-50 C ambient plus self-heating: about 15 C of headroom at best.
- Sources: <https://docs.waveshare.com/ESP32-S3-Touch-LCD-4.3>, <https://www.waveshare.com/wiki/ESP32-S3-Touch-LCD-4.3>, <https://docs.waveshare.com/ESP32-S3-Touch-LCD-7>

### Waveshare ESP32-S3-Touch-LCD-3.5 / 3.5B

- 3.5 in IPS 320x480, ST7796, FT6336 touch, 16 MB flash, 8 MB PSRAM, Type-C, 2.54 mm GPIO header (pin list not verified). Operating temperature and dimensions not in the extracted docs.
- Source: <https://docs.waveshare.com/ESP32-S3-Touch-LCD-3.5>

### Waveshare ESP32-S3-Touch-LCD-2.8

- ST7789 240x320 IPS with CST328 touch; native USB-C ("USB CDC On Boot" must be enabled for Serial); 73.06 x 50.54 mm. A 12-pin connector carries TXD (GPIO43), RXD (GPIO44), IO18, IO15 and VBUS 5V. Four confirmed spare pins gives two channels; a third channel and mounting holes are unverified.
- Source: <https://www.waveshare.com/wiki/ESP32-S3-Touch-LCD-2.8>

### M5Stack Basic v2.7 / Core2 / CoreS3 / Tough / StickC Plus2 / Dial

- Basic v2.7: ESP32-D0WDQ6-V3, 16 MB, 2.0 in ILI9342C IPS at 853 nits (highest published brightness in this survey), CH9102F bridge, USB-C, 5 V 500 mA input, 110 mAh battery, 54 x 54 x 17 mm. M-Bus exposes many GPIOs. Operating temperature not published on the docs page. Enclosure is a finished plastic case; access to the M-Bus requires a base or proto module.
- Core2 v1.1: 0 to 60 C, 46.90 USD, marked EOL; v1.3 replaces it.
- CoreS3: ESP32-S3, 16 MB + 8 MB PSRAM, ILI9342C 2.0 in capacitive IPS, native USB-C, ports A/B/C plus M-Bus, 500 mAh battery. Temperature not published.
- Tough: 2.0 in 853 nits, CH9102, four HY2.0-4P ports (A-D), RS485 6-24 V input with DC-DC, described as dustproof/waterproof (not immersion-rated), 76 x 58 x 41.6 mm, structure files on GitHub. Port pins: G32, G33, G26, G36, G14, G13, G27, G19. Temperature not published.
- StickC Plus2: 0 to 40 C, marked EOL. Excluded on temperature.
- Dial: not verified.
- M5Stack built-in LiPo batteries are a risk at 40-50 C ambient (battery temperature limits not verified; typical LiPo charge limits are 0-45 C).
- M5Stack libraries: M5Unified / M5GFX, mature and well maintained, plus LVGL ports.
- Sources: <https://docs.m5stack.com/en/core/basic_v2.7>, <https://docs.m5stack.com/en/core/CoreS3>, <https://docs.m5stack.com/en/core/Tough>, <https://shop.m5stack.com/products/m5stack-core2-esp32-iot-development-kit-v1-1>, <https://docs.m5stack.com/en/core/M5StickC%20PLUS2>

## USB Serial and Auto-Reset

- Boards with a dedicated bridge chip (CH340, CP2102, CH9102, CH343P): Heltec V3 (CP2102), CYD (CH340), M5Stack Basic/Core2/Tough (CH9102), Waveshare 4.3 second port (CH343P). Behaviour is the classic Espressif DTR/RTS reset circuit: the host toggling DTR/RTS can reset or put the chip in bootloader mode. Typical port-open leaves both lines asserted, which is a no-op in the standard circuit, but an ordering glitch can still reset the chip. Test with Artisan's port-open path on the actual Pi.
- Boards with native USB (T-Display-S3, Adafruit S3 Feather, CoreS3, Waveshare S3 boards): the S3 CDC-ACM uses virtual RTS/DTR; the chip resets if the lines are toggled in a certain sequence. In hardware-CDC mode (USB-Serial/JTAG), reset via DTR/RTS cannot be disabled on the S3 (as reported by one source). The Arduino-ESP32 USB CDC API has `enableReboot()` to control this in TinyUSB CDC mode. Mitigations: open the port with DTR/RTS pre-set (pyserial `dsrdtr=False`, `rtscts=False`), or firmware using TinyUSB CDC with reboot disabled. Whether Artisan's serial library triggers a reset on open is unverified. It should be tested on a Pi before committing.
- Other native-USB considerations that were not verified in this pass: the port re-enumerates (a new /dev/ttyACMx) on any reset, and Serial writes with no host attached may block depending on core version.
- Sources: <https://docs.espressif.com/projects/arduino-esp32/en/latest/api/usb_cdc.html>, <https://qsantos.fr/2025/05/09/espressifs-automatic-reset/>, <https://github.com/espressif/arduino-esp32/issues/8237>, <https://forum.arduino.cc/t/esp32-reset-at-serial-terminal-shutdown/1391969>

## Temperature and Heat

Only a few boards publish a temperature range. Verified from vendor pages: Waveshare 4.3/7 in 0 to 65 C; CrowPanel 5.0 in -20 to 70 C (and 7 in P4 -20 to 70 C); Heltec WiFi Kit 32 V3 -20 to 70 C; M5Stack Core2 v1.1 0 to 60 C; M5StickC Plus2 0 to 40 C; CrowPanel 4.2 in e-paper 0 to 50 C. For LilyGO T-Display-S3, Adafruit, CYD, M5Stack Basic/CoreS3/Tough and Waveshare 2.8/3.5, no range was found (unverified). The ESP32-S3 module silicon is normally rated to 85 C (from Espressif module datasheets; not re-verified here), so the limiting parts are likely the LCD panel, LiPo cells and the enclosure heat. A design that puts the display in the enclosure lid, away from the roaster, and uses no battery, is safest. The current custom-PCB plan (bare module plus an external LCD) keeps the displayed part separate, but the HD44780-class LCD's own temperature range is also unverified in the project notes.

No published heat problems for these boards were found; that is absence of evidence, not a clean bill of health.

## Verdict: Is an Integrated-Display Board Better Than Bare Module + LCD?

- Advantages: no LCD, I2C backpack or BSS138 level shifters; the LCD's 5V supply and 98 x 60 mm footprint go away; ready-made libraries; cheap enough (about 13-40 USD) to buy spares.
- Disadvantages: displays 1.1-1.9 in are much smaller than a 20x4 character LCD; no board except the M5Stack Basic publishes a brightness figure; temperature ratings mostly missing; native USB reset behaviour needs testing with Artisan; a custom carrier PCB is still needed for the three isolated breakouts, the 5V distribution and connectors; cases are often unofficial.
- The integrated board can save cost and effort but is not clearly superior. The strongest case is a cheap, replaceable module (T-Display-S3) on a carrier PCB.

## Ranked Shortlist

1. **LilyGO T-Display-S3 (non-touch, about 25 USD).** PASS-3: six clean header GPIOs plus the SPI-labelled pins, 5V on the header, BOOT and IO14 buttons already onboard, 1.9 in IPS 170x320 is the largest readable panel among boards that pass at 3 channels, 16 MB flash. Caveats: native USB CDC reset behaviour must be tested with Artisan, temperature and nits unpublished, no mounting holes, 5V pin current path to be confirmed from the schematic.
2. **Adafruit ESP32-S3 Reverse TFT Feather (24.95 USD).** PASS-3 with the best pin story (A0-A5, D5, D6, D9-D13, SPI), a "USB" pin, three user buttons, display on the back for panel mounting, and the best documentation and support longevity. Caveats: smallest display (1.14 in, 240x135), native USB, no published temperature.
3. **M5Stack Basic v2.7 (about 30-40 USD, unverified price).** PASS-3 through the M-Bus, dedicated CH9102F bridge (avoids native-CDC reset), brightest published display (853 nits IPS), finished case. Caveats: display is 2.0 in but the M-Bus needs a base module for wiring, the 110 mAh LiPo is a risk at 40-50 C (remove or avoid), operating temperature not published.
4. **M5Stack Tough (about 55-60 USD, unverified price).** Four HY2.0 ports give enough pins for three channels through Grove-style cables, 853 nit display, CH9102 bridge, robust case with a published structure file for mounting, and 6-24 V RS485-port input as an alternative supply. Caveats: expensive, small port connectors, temperature unpublished. Fallback alternative: Heltec WiFi Kit 32 V3 (CP2102, -20 to 70 C published) if a 0.96 in OLED display were acceptable, which it probably is not.

Not recommended: CYD family and Sunton/Waveshare/Elecrow RGB panels (too few free pins), M5StickC Plus2 (0-40 C, EOL), Core2 v1.1 (EOL), AMOLED variants (burn-in and unpublished brightness).

## Unverified Items Summary

Operating temperature for T-Display-S3, Adafruit, CYD, M5 Basic/CoreS3/Tough; nits for all but M5Stack (853) and Waveshare 4.3 (270); VBUS current path on every board; TTGO T-Display details; AMOLED GPIO list; CoreS3 free pin count; Waveshare 3.5 and 2.8 third-channel pins; CrowPanel GPIO repurposing; Dial; mounting holes for most boards; whether Artisan's port open resets a native-USB S3.

## Sources

- <https://lilygo.cc/products/t-display-s3>
- <https://www.espboards.dev/esp32/lilygo-t-display-s3/>
- <https://protosupplies.com/product/lilygo-t-display-s3/>
- <https://protosupplies.com/product/lilygo-t-display-s3-touch/>
- <https://wiki.lilygo.cc/products/t-display-series/t-display-s3-amoled/>
- <https://lilygo.cc/en-us/products/t-display-s3-amoled>
- <https://www.tindie.com/products/lilygo/lilygo-t-display-s3-esp32-s3-with-191inch-amoled/>
- <https://www.adafruit.com/product/5691>
- <https://learn.adafruit.com/esp32-s3-reverse-tft-feather/pinouts>
- <https://learn.adafruit.com/esp32-s3-reverse-tft-feather/overview>
- <https://heltec.org/project/wifi-kit32-v3/>
- <https://www.espboards.dev/esp32/heltec-wifi-kit-32-v3/>
- <https://randomnerdtutorials.com/esp32-cheap-yellow-display-cyd-pinout-esp32-2432s028r/>
- <https://github.com/witnessmenow/ESP32-Cheap-Yellow-Display/blob/main/PINS.md>
- <https://www.espboards.dev/esp32/cyd-esp32-2432s028/>
- <https://www.atomic14.com/esp32/boards/sunton-esp32-8048s070/>
- <https://www.openhasp.com/0.7.0/hardware/sunton/esp32-8048s0xx/>
- <https://www.elecrow.com/wiki/esp32-display-282727-intelligent-touch-screen-wi-fi26ble-240320-hmi-display.html>
- <https://github.com/Elecrow-RD/CrowPanel-5.0-HMI-ESP32-Display-800x480>
- <https://www.makerguides.com/elecrow-2-8-esp32-display-setup-guide/>
- <https://docs.waveshare.com/ESP32-S3-Touch-LCD-4.3>
- <https://www.waveshare.com/wiki/ESP32-S3-Touch-LCD-4.3>
- <https://docs.waveshare.com/ESP32-S3-Touch-LCD-7>
- <https://docs.waveshare.com/ESP32-S3-Touch-LCD-3.5>
- <https://www.waveshare.com/wiki/ESP32-S3-Touch-LCD-2.8>
- <https://docs.m5stack.com/en/core/basic_v2.7>
- <https://docs.m5stack.com/en/core/CoreS3>
- <https://docs.m5stack.com/en/core/Tough>
- <https://docs.m5stack.com/en/core/M5StickC%20PLUS2>
- <https://shop.m5stack.com/products/m5stack-core2-esp32-iot-development-kit-v1-1>
- <https://docs.espressif.com/projects/arduino-esp32/en/latest/api/usb_cdc.html>
- <https://qsantos.fr/2025/05/09/espressifs-automatic-reset/>
- <https://github.com/espressif/arduino-esp32/issues/8237>
- <https://forum.arduino.cc/t/esp32-reset-at-serial-terminal-shutdown/1391969>
- <https://www.cnx-software.com/2025/12/27/esp32-c6-amoled-development-board-touch-display-built-in-mic-and-speaker-imu-rtc/>
- <https://www.cnx-software.com/2025/09/16/esp32-s3-wide-touch-display-development-board-features-a-640x172-touch-lcd-ai-voice-support/>
