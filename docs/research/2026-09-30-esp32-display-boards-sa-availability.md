# ESP32 boards with built-in display: South African availability and pricing

Research date: 30 September 2026. Prices were read from live supplier pages or supplier APIs on this date. Exchange rate used for USD conversions: R16.41 per US$1 (open.er-api.com, 30 September 2026).

## Summary

- The current design (bare ESP32 plus a Keyestudio MD0074 20x4 LCD) was priced at R184.47 ex-VAT for the LCD and R238.20 ex-VAT for the KS5019 dev board, about R422.67 ex-VAT (R486.07 incl. VAT) together.
- The cheapest integrated-display option that is genuinely in stock locally is the 2.8" "Cheap Yellow Display" (CYD) style board: **DIY Electronics R387.00 incl. VAT (R336.52 ex-VAT)**, "last items" stock. Takealot has the same class of board at R498.00 incl. VAT in stock. Both are about the same cost as the current LCD plus dev board, and give a graphical colour touchscreen instead of 20x4 characters.
- Micro Robotics, the usual local source for Waveshare, Makerfabs and LILYGO boards, showed **no stock at any branch on any of its 32 ESP32-with-display products** on 30 September 2026. Its prices are lower than most, so it is worth re-checking.
- Mantech lists no ESP32 board with an integrated display. Its only match was a TTGO LoRa32 OLED, "restocking soon", no price shown. Note that the KS5019 dev board (16K7268-MANTECH-KZN) also shows "Restocking soon".
- The widest genuine range is DigiKey South Africa (M5Stack Core2, CoreS3, Basic, Tough, Dial; Adafruit TFT Feathers; DFRobot; 4D Systems), but it is priced ex-VAT and adds shipping plus import VAT and a clearance fee (see the DigiKey section).
- The best import value is a CYD from AliExpress or a LILYGO T-Display-S3 from LILYGO direct, but after courier handling fees the saving over local stock is small or nil for a single unit.

## Suitability note for a roaster monitor

The design needs three MAX31855 SPI thermocouple amplifiers (shared SCK and MISO, three chip-select lines), so about five free GPIOs besides the display. Board pinouts were not checked in this research. Many CYD-type boards break out only a few spare GPIOs, and some of those are input-only, so confirm the pinout before choosing. M5Stack boards expose I2C/SPI through their headers and Grove ports, and the Adafruit TFT Feathers expose plenty of pins.

## Locally stocked boards, by supplier

Price basis: "Ex-VAT" and "Incl. VAT" are both shown. The basis actually printed by the supplier is: DIY Electronics incl. VAT (its page data shows R336.52 ex-VAT for the R387.00 CYD), Micro Robotics ex-VAT with an "Inc Tax" figure, Communica ex-VAT (each price is an exact multiple of 1.15 when VAT is added), DigiKey ZA ex-VAT, Robofactory incl. VAT (VAT 15% in page data), Netram incl. VAT (page shows "R460.87 (ex VAT)" for R530), PiShop incl. VAT, Takealot incl. VAT. The other column is calculated at 15%.

Stock status: as shown on the page or in the site's own product data on 30 September 2026. DigiKey ZA lines are stock held by DigiKey, not a local shelf, so they need international shipping (see below).

| Supplier | Product | SKU / stock code | Ex-VAT | Incl. VAT | Stock | URL |
|---|---|---|---|---|---|---|
| Communica | BMT ESP32 LVGL+WIFI+BT+3.5IN LCD (3.5" TFT touch) | BMT ESP32 LVGL+WIFI+BT+3.5IN LCD | R456.52 | R525.00 | In stock (Samrand branch only) | https://www.communica.co.za/products/bmt-esp32-lvgl-wifi-bt-3-5in-lcd |
| Communica | HKD ESP32+WIFI+BT+OLED+BATT HOLD (0.96" OLED, Wemos-style) | HKD ESP32+WIFI+BT+OLED+BATT HOLD | R365.22 | R420.00 | In stock (Samrand branch only) | https://www.communica.co.za/products/hkd-esp32-wifi-bt-oled-batt-hold |
| Communica | BMT ESP32 LVGL+WIFI+BT+2.8IN LCD (CYD-type) | BMT ESP32 LVGL+WIFI+BT+2.8IN LCD | R347.83 | R400.00 | Out of stock | https://www.communica.co.za/products/bmt-esp32-lvgl-wifi-bt-2-8in-lcd |
| Communica | BDD ESP32 LVGL+WIFI+BT+2.8IN LCD (CYD-type) | BDD ESP32 LVGL+WIFI+BT+2.8IN LCD | R413.04 | R475.00 | Out of stock | https://www.communica.co.za/products/bdd-esp32-lvgl-wifi-bt-2-8in-lcd |
| Communica | Waveshare ESP32-S2 MCU WiFi board + LCD | WVS ESP32-S2 MCU WIFI BOARD+LCD | R295.65 | R340.00 | Out of stock | https://www.communica.co.za/products/wvs-esp32-s2-mcu-wifi-board-lcd |
| Communica | Waveshare ESP32-S3-Touch-LCD-1.28 + gyro | WVS ESP32-S3-TOUCH-LCD-1.28+GYRO | R430.43 | R494.99 | Out of stock | https://www.communica.co.za/products/wvs-esp32-s3-touch-lcd-1-28-gyro |
| Communica | Waveshare ESP32-S3-Touch-AMOLED-1.64 | WVS ESP32-S3-TOUCH-AMOLED-1.64 | R513.04 | R590.00 | Out of stock | https://www.communica.co.za/products/wvs-esp32-s3-touch-amoled-1-64 |
| Communica | Waveshare ESP32-S3 4.3" dev board | WVS ESP32-S3 4.3INCH DEV BOARD | R765.22 | R880.00 | Out of stock | https://www.communica.co.za/products/wvs-esp32-s3-4-3inch-dev-board |
| DigiKey ZA | DFRobot 2" ESP32-S3 IPS screen | DFR0997 | R240.46 | R276.53 | 35 in stock | https://www.digikey.co.za/en/products/detail/dfrobot/DFR0997/24854504 |
| DigiKey ZA | Adafruit ESP32-S3 Reverse TFT Feather (1.14" TFT) | 5691 | R402.64 | R463.04 | 1,627 in stock | https://www.digikey.co.za/en/products/detail/adafruit-industries-llc/5691/18627502 |
| DigiKey ZA | Adafruit ESP32-S3 TFT Feather (front TFT) | 5483 | R402.64 | R463.04 | 69 in stock | https://www.digikey.co.za/en/products/detail/adafruit-industries-llc/5483/16592513 |
| DigiKey ZA | DFRobot ESP32-S3 round touch display board | DFR1221 | R562.89 | R647.32 | 11 in stock | https://www.digikey.co.za/en/products/detail/dfrobot/DFR1221/28531126 |
| DigiKey ZA | M5Stack Basic Core ESP32 IoT dev kit V2.7 (2" TFT) | K001-V27 | R643.91 | R740.50 | 620 in stock | https://www.digikey.co.za/en/products/detail/m5stack-technology-co-ltd/K001-V27 |
| DigiKey ZA | M5Stack Core2 ESP32 IoT dev kit v1.3 (2" touch) | K010-V13 | R692.32 | R796.17 | 94 in stock | https://www.digikey.co.za/en/products/detail/m5stack-technology-co-ltd/K010-V13/29427556 |
| DigiKey ZA | M5Stack CoreS3 SE IoT controller | K128-SE | R627.77 | R721.94 | 331 in stock | https://www.digikey.co.za/en/products/detail/m5stack-technology-co-ltd/K128-SE/23628221 |
| DigiKey ZA | M5Stack CoreS3 ESP32-S3 IoT dev kit | K128 | R966.67 | R1,111.67 | 596 in stock | https://www.digikey.co.za/en/products/detail/m5stack-technology-co-ltd/K128/18839257 |
| DigiKey ZA | M5Stack Tough ESP32 IoT dev kit | K034 | R805.29 | R926.08 | 88 in stock | https://www.digikey.co.za/en/products/detail/m5stack-technology-co-ltd/K034 |
| DigiKey ZA | M5Stack Dial v1.1 (1.28" round touch) | K130-V11 | R563.22 | R647.70 | 515 in stock | https://www.digikey.co.za/en/products/detail/m5stack-technology-co-ltd/K130-V11/26267933 |
| DigiKey ZA | 4D Systems GEN4-ESP32-28 (2.8" TFT, no touch) | GEN4-ESP32-28 | R790.76 | R909.37 | 9 in stock | https://www.digikey.co.za/en/products/detail/4d-systems-pty-ltd/GEN4-ESP32-28/21762967 |
| DigiKey ZA | 4D Systems GEN4-ESP32-35 (3.5" TFT, no touch) | GEN4-ESP32-35 | R1,113.52 | R1,280.55 | 16 in stock | https://www.digikey.co.za/en/products/detail/4d-systems-pty-ltd/GEN4-ESP32-35/21762997 |
| DigiKey ZA | Espressif ESP32-S3-BOX-3 | ESP32-S3-BOX-3 | R790.76 | R909.37 | 0 in stock | https://www.digikey.co.za/ |
| DIY Electronics | 2.8inch LCD Touchscreen ESP32 CYD Module (ILI9341, resistive touch) | ESP32CYD | R336.52 | R387.00 | In stock, low ("last items", 5 units) | https://www.diyelectronics.co.za/store/iot/5622-8inch-lcd-touchscreen-esp32-cyd-module-wifibluetooth.html |
| DIY Electronics | TTGO ESP32 T-Display Dev Board, 1.14" LCD | 9MTTGOTDISP1 | R375.65 | R432.00 | In stock, low ("last items") | https://www.diyelectronics.co.za/store/iot/3622-ttgo-esp32-t-display-dev-board-for-arduino-114-lcd-wifi-ble.html |
| DIY Electronics | LilyGo TTGO ESP32-S3 T-QT Display Module V1.1, 0.85" LCD | 9MTTLILYGOLCD | R340.87 | R392.00 | In stock | https://www.diyelectronics.co.za/store/iot/4364-lilygo-ttgo-esp32-s3-t-qt-display-module-v11-085-lcd-wifi-ble.html |
| DIY Electronics | Smart Round ESP32-S3 IPS LCD Display, 1.28" | 9MWE32S3LR | R333.91 | R384.00 | In stock | https://www.diyelectronics.co.za/store/motion/5725-smart-round-esp32-s3-ips-lcd-display-128-inch.html |
| DIY Electronics | Smart Round ESP32-S3 Touch LCD, 1.28" | 9MWE32S3LRT | R441.74 | R508.00 | In stock | https://www.diyelectronics.co.za/store/motion/5723-smart-round-esp32-s3-touch-lcd-128-inch.html |
| DIY Electronics | Smart Round ESP32-S3 IPS LCD, 1.28" with metal case | 9MWE32S3LRC | R407.83 | R469.00 | In stock | https://www.diyelectronics.co.za/store/motion/5724-smart-round-esp32-s3-ips-lcd-display-128-inch-with-metal-case.html |
| DIY Electronics | Smart Round ESP32-S3 Touch LCD, 1.28" with metal case | 9MWE32S3LRTC | R515.65 | R593.00 | Out of stock | https://www.diyelectronics.co.za/store/motion/5722-smart-round-esp32-s3-touch-lcd-128-inch-with-metal-case.html |
| DIY Electronics | Smart ESP32-S3 Touch LCD, 1.69" rectangular | 9MWE32S3LT | R421.74 | R485.00 | Out of stock | https://www.diyelectronics.co.za/store/motion/5726-smart-esp32-s3-touch-lcd-169-inch-rectangular.html |
| DIY Electronics | ESP32-S3 Knob Touch Display Dev Board, 1.8" with metal case | 9MWE32S3RKM | R955.65 | R1,099.00 | In stock | https://www.diyelectronics.co.za/store/iot/7074-esp32-s3-knob-touch-display-dev-board-18-inch-with-metal-case.html |
| DIY Electronics | ESP32-S3 RGB LCD Driver Board with 2.8" round touchscreen | WE32S3DDBR2.8 | R715.65 | R823.00 | Listed "discontinued"; page shows last items | https://www.diyelectronics.co.za/store/iot/5746-esp32-s3-rgb-lcd-driver-board-with-28-inch-round-touchscreen.html |
| DIY Electronics | TTGO T2 ESP32 WiFi Dev Board, 0.95" OLED + SD | 9MESP32TTGOT2 | R607.83 | R699.00 | In stock | https://www.diyelectronics.co.za/store/iot/6251-ttgo-t2-esp32-wifi-dev-board-095-oled-sd-card-slot.html |
| DIY Electronics | TTGO LoRa32 V2.1 WiFi Dev Board, 0.96" OLED | 9MT32V2.1868 | R778.26 | R895.00 | In stock | https://www.diyelectronics.co.za/store/iot/6647-ttgo-lora32-v21-wifi-dev-board-096-oled-antenna.html |
| DIY Electronics | LilyGo T3S3 ESP32-S3 LoRa, 0.96" OLED | 9ME32T8LT3S3 | R599.13 | R689.00 | Out of stock | https://www.diyelectronics.co.za/store/iot/5626-lilygo-t3s3-esp32-s3-sx1262-lora-display-dev-board-096-wifi-ble.html |
| DIY Electronics | ESP32-C3 Mini dev board, 0.42" OLED | ESP32C3O42 | R286.09 | R329.00 | Out of stock | https://www.diyelectronics.co.za/store/led-displays/5621-esp32-c3-mini-wifible-dev-board-042-inch-oled.html |
| DIY Electronics | UNIHIKER K10 AI board (ESP32-S3, colour screen) | DEV-1001 | R607.83 | R699.00 | Out of stock | https://www.diyelectronics.co.za/store/iot/7461-unihiker-k10-ai-agent-coding-board-for-stem-maker.html |
| Mantech | TTGO LoRa32 V2.1 ESP32 OLED 0.96" (99K4886-MANTECH-KZN) | XY241009 | n/a | n/a | Restocking soon; no price shown | https://www.mantech.co.za/ |
| Micro Robotics | CYD ESP32 2.8" Resistive Touch Display | E32R28T | R298.00 | R342.70 | No stock (Centurion, Stellenbosch, Bulk) | https://www.robotics.org.za/E32R28T |
| Micro Robotics | LILYGO T-Display ESP32-S3 1.9" LCD | H577 | R315.00 | R362.25 | No stock (Centurion, Stellenbosch, Bulk) | https://www.robotics.org.za/H577 |
| Micro Robotics | ESP32-S3 SPI TFT with Touch 3.5" ILI9488 | ESP32S3SPI35 | R498.00 | R572.70 | No stock (Centurion, Stellenbosch, Bulk) | https://www.robotics.org.za/ESP32S3SPI35 |
| Micro Robotics | MaTouch ESP32-S3 Resistive Touch 2.4" ST7789 | MALI24R | R268.00 | R308.20 | No stock (Centurion, Stellenbosch, Bulk) | https://www.robotics.org.za/MALI24R |
| Micro Robotics | MaTouch ESP32-S3 Resistive Touch 3.95" ST7796 | MALI395R | R388.00 | R446.20 | No stock (Centurion, Stellenbosch, Bulk) | https://www.robotics.org.za/MALI395R |
| Micro Robotics | Wave ESP32-S3 2.8" Touch IPS Display | W27690 | R556.00 | R639.40 | No stock (Centurion, Stellenbosch, Bulk) | https://www.robotics.org.za/W27690 |
| Micro Robotics | Wave ESP32-S3 4.3" Display | W25948 | R748.00 | R860.20 | No stock (Centurion, Stellenbosch, Bulk) | https://www.robotics.org.za/W25948 |
| Micro Robotics | MaESP ESP32-C3 Board with 1.3" OLED | MAESPC3OL | R198.00 | R227.70 | No stock (Centurion, Stellenbosch, Bulk) | https://www.robotics.org.za/MAESPC3OL |
| Micro Robotics | ESP32-C6 Dev Board with onboard 1.47" Display | W30381 | R238.00 | R273.70 | No stock (Centurion, Stellenbosch, Bulk) | https://www.robotics.org.za/W30381 |
| Netram | ESP32 CYD WiFi & Bluetooth 2.8" LCD touch display | DIS-00090 | R460.87 | R530.00 | Back-order (out of stock) | https://www.netram.co.za/wifi/11055-esp32-cyd-wifi-bluetooth-28-inch-lcd-touch-display.html |
| PiShop | ESP32 OLED Module (Wemos LOLIN-style, 0.96" OLED) | ESP32 with OLED display | R104.26 | R119.90 | 18 in stock | https://www.pishop.co.za/store/wemos-lolin-esp32---wifi---bluetooth-dual-esp-32-esp-32s-esp8266-oled-module |
| PiShop | Waveshare ESP32-S3 5" Display Dev Board (ESP32-S3-Touch-LCD-5B) | ESP32-S3-Touch-LCD-5B | R869.47 | R999.89 | Out of stock | https://www.pishop.co.za/store/esp32-s3-5inch-display-development-board-32-bit-lx7-dual-core-processor-up-to-240mhz-frequency-supports-wifi |
| Robofactory | M5Stack Dial ESP32-S3 (list R990.00, shown price R940.50) | 1004 | R817.83 | R940.50 | In stock (1) | https://www.robofactory.co.za/m5stack/1004-m5stack-dial-esp32-s3-smart-rotary-knob.html |
| Robofactory | M5Stack Core2 IoT Dev Kit for AWS EduKit (list R1,250.00) | 431 | R1,032.61 | R1,187.50 | In stock (2) | https://www.robofactory.co.za/m5stack/431-m5stack-core2-esp32-iot-development-kit-for-aws-iot-edukit.html |
| Robofactory | M5Stack Core2 ESP32 IoT Dev Kit (list R1,195.00) | 429 | R987.17 | R1,135.25 | Not enough stock | https://www.robofactory.co.za/m5stack/429-m5stack-core2-esp32-iot-development-kit.html |
| Robofactory | M5Stack FIRE IoT Dev Kit PSRAM V2.6 (list R1,195.00) | 430 | R987.17 | R1,135.25 | Back-order | https://www.robofactory.co.za/m5stack/430-m5stack-fire-iot-development-kit-psram-v26.html |
| Robofactory | TTGO T-Display ESP32 1.14" (list R455.00) | 176 | R375.87 | R432.25 | Back-order | https://www.robofactory.co.za/esp-controllers/176-ttgo-t-display-esp32-114-inch-wifi-module.html |
| Takealot (marketplace) | ESP32 2.8" TFT Touch Screen Dev Board 240x320 IPS (KR104) | PLID102577365 | R433.04 | R498.00 | In stock | https://www.takealot.com/esp32-2-8-tft-touch-screen-development-board-240x320-ips-display/PLID102577365 |
| Takealot (marketplace) | ESP32 Development Board WiFi 2.8" Smart Display Touch Screen | PLID102132991 | R433.04 | R498.00 | In stock (from R498) | https://www.takealot.com/esp32-development-board-wifi-2-8-inch-smart-display-touch-screen/PLID102132991 |
| Takealot (marketplace) | ESP32-S3 3.5" Capacitive Touch IPS Display Dev Board | PLID99264460 | R555.65 | R639.00 | In stock | https://www.takealot.com/esp32-s3-3-5-inch-capacitive-touch-ips-display-development-board/PLID99264460 |
| Takealot (marketplace) | BMT ESP32 LVGL WiFi BT 3.5" TFT Touch Display Board | PLID101535158 | R651.30 | R749.00 | Ships in 4-6 work days | https://www.takealot.com/bmt-esp32-lvgl-wifi-bluetooth-3-5-tft-touch-display-board/PLID101535158 |
| Takealot (marketplace) | LILYGO T-Display-S3 ESP32-S3 1.9" ST7789 | PLID102647635 | R646.09 | R743.00 | Ships in 18-20 work days | https://www.takealot.com/lilygo-t-display-s3-esp32-s3-1-9inch-st7789-display-development-/PLID102647635 |
| Takealot (marketplace) | HKD Wemos ESP32 WiFi/BT module with OLED + battery holder | PLID98450652 | R520.87 | R599.00 | Ships in 4-6 work days | https://www.takealot.com/hkd-wemos-esp32-wifi-bluetooth-module-with-oled-display-battery-/PLID98450652 |
| Takealot (marketplace) | BDD ESP32 2.8" LCD Touch Display Dev Board | PLID98307691 | R415.65 | R478.00 | Supplier out of stock | https://www.takealot.com/bdd-esp32-2-8-lcd-touch-display-development-board/PLID98307691 |

DigiKey ZA prices exclude shipping (free at or above R2,000 ex-VAT, otherwise R600 per the local `dk` tool notes), import VAT and courier clearance fees.

Micro Robotics lists 32 ESP32-with-display products in its "ESP32 with onboard Display" category, all with "No Stock" at Centurion, Stellenbosch and Bulk on 30 September 2026. The nine most relevant are in the table above. Others (all no stock) include Wave ESP32-S3 4" R657 ex, 5" R846 ex, 7" R804 ex, 1.47" R252 ex, 1.64" AMOLED R524 ex, and MaTouch 1.9" R538 ex.

### Suppliers checked with nothing suitable, or not verifiable

| Supplier | Result |
|---|---|
| Mantech (mantech.co.za) | Search works only via its own form. Queries for esp32 display, lcd, tft, oled, m5stack, lilygo, ttgo, waveshare, heltec found no ESP32 board with a screen apart from the TTGO LoRa32 OLED (restocking soon, no price). KS5019 shows "Restocking soon". MD0074 is listed under 15M8244, 15K4477-MANTECH-KZN and 15M8244-MANTECH-EC. |
| Leobot (leobot.net) | Scanned all 1,292 products across its categories. Only ESP32-CAM (5163) and DFRobot Beetle ESP32 (4370) matched. No ESP32 display board. |
| Botshop (botshop.co.za) | Now redirects to a robotics education platform (botshop.co.za), no product catalogue or prices found. |
| RS South Africa (za.rs-online.com) | Blocked automated access (HTTP 403). Could not verify. |
| DigiKey ZA website | Blocked by Cloudflare for direct page fetches. Prices above came from the DigiKey API via the local `dk` tool, which reads the digikey.co.za catalogue. Product page URLs were returned by the API. |
| Robofactory | Only the M5Stack and TTGO items in the table. No CYD, Waveshare or Heltec found. |
| Netram | Only the CYD in the table. |
| PiShop | ESP32 OLED module and the Waveshare 5" board only. Site search was awkward, so smaller items could have been missed. |
| Heltec, Elecrow CrowPanel, Seeed display products | No local stockist found by any supplier search. Elecrow and Seeed items appear on DigiKey ZA only (Elecrow CrowPanel lines showed 0 stock; Seeed XIAO ESP32-S3 display boards showed 0 stock). |

## Import route

### Direct prices seen on manufacturer pages (30 September 2026)

| Board | Source | Price seen (US$) | ZAR at R16.41 | URL |
|---|---|---|---|---|
| LILYGO T-Display-S3, H577 soldered pin, 1.9" LCD | LILYGO store, China "for worldwide" variant | $9.54 | R156.53 | https://lilygo.cc/products/t-display-s3 |
| LILYGO T-Display-S3 AMOLED V2.0 (H712) / Touch (H705) | LILYGO store, China worldwide | $26.94 / $30.44 | R442 / R499 | https://lilygo.cc/products/t-display-s3-amoled |
| LILYGO T-Display (1.14", original) 4MB | LILYGO store | $8.04 | R131.91 | https://lilygo.cc/products/t-display |
| Waveshare ESP32-S3-Touch-LCD-2.8 | Waveshare store, price range across options | $19.99 to $25.99 | R328 to R426 | https://www.waveshare.com/esp32-s3-touch-lcd-2.8.htm |
| Waveshare ESP32-S3-Touch-LCD-3.5 | Waveshare store, range | $25.99 to $32.99 | R426 to R541 | https://www.waveshare.com/esp32-s3-touch-lcd-3.5.htm |
| Waveshare ESP32-S3-Touch-LCD-4.3 | Waveshare store, range | $27.99 to $32.99 | R459 to R541 | https://www.waveshare.com/esp32-s3-touch-lcd-4.3.htm |
| M5Stack Core2 v1.3 | M5Stack store | $42.90 | R703.9 | https://shop.m5stack.com/products/m5stack-core2-esp32-iot-development-kit-v1-3 |
| M5Stack CoreS3 SE | M5Stack store | $38.90 | R638.3 | https://shop.m5stack.com/products/m5stack-cores3-se-iot-controller-w-o-battery-bottom |
| M5Stack Dial v1.1 | M5Stack store | $34.90 | R572.6 | https://shop.m5stack.com/products/m5stack-dial-v1-1 |
| 2.8" CYD ESP32-2432S028R | AliExpress and eBay, from search-result snippets only (not opened on the seller page) | about $8 on AliExpress, $18.98 seen on eBay | about R131 to R311 | see Sources |

Notes: the Waveshare page shows a price range, and the low end applies to the base variant. The LILYGO store's "China [For Worldwide]" variants are the cheapest, with Germany and US variants costing more. The M5Stack Core2 page also lists an older v1.1 at $46.90. M5StickC PLUS2 is shown as end-of-life ("EOL") on the M5Stack store.

### What a South African buyer pays landed

Method, from the sources below: import VAT of 15% is charged on the Added Tax Value, which is (customs value x 1.10) plus duty. Customs value includes shipping. Duty on ESP32 boards and displays is typically 0% to 9% for electronics (jlog.co.za); I assumed 0% duty. The courier then adds a handling or clearance fee, quoted at R100 to R500 per parcel (jlog.co.za) or R200 to R600 for DHL, FedEx and Aramex (evetech.co.za).

Shipping figures are my assumptions, not seen prices. Please treat the landed figures as illustrative.

| Board | Goods (US$) | Assumed shipping (US$) | Goods plus shipping | Import VAT | Before courier fee | With R100 to R500 fee |
|---|---|---|---|---|---|---|
| CYD 2.8" (AliExpress, about $8) | 8.00 | 3 | R180.48 | R29.78 | R210.25 | R310 to R710 |
| LILYGO T-Display-S3 (H577) | 9.54 | 15 | R402.63 | R66.43 | R469.06 | R569 to R969 |
| Waveshare 2.8" | 19.99 | 20 | R656.11 | R108.26 | R764.37 | R864 to R1,264 |
| LILYGO T-Display-S3 AMOLED Touch (H705) | 30.44 | 15 | R745.53 | R123.01 | R868.54 | R969 to R1,369 |
| Waveshare 3.5" | 25.99 | 20 | R754.56 | R124.50 | R879.06 | R979 to R1,379 |
| M5Stack Core2 v1.3 | 42.90 | 25 | R1,114.03 | R183.82 | R1,297.85 | R1,398 to R1,798 |

Comparison: for one unit, a courier handling fee plus shipping erases most of the price advantage. A CYD landed via courier is realistically R310 to R710, against R387.00 incl. VAT at DIY Electronics and R498.00 at Takealot. Ordering several boards in one parcel spreads the handling fee and shipping, which is where importing pays off.

### Current SA rules on low-value parcels (verified position and its limits)

- SARS media release of 8 August 2024: the old concession (flat 20% duty and no VAT on goods of R500 or less) was to be replaced. VAT was added on top of the 20% flat rate from 1 September 2024, and from 1 November 2024 the flat rate was to be reconfigured into World Customs Organization categories with normal duty rates.
- The 2025 Draft Taxation Laws Amendment Bill proposes removing the R500 VAT exemption in law (Baker McKenzie, VATupdate). I could not confirm from a primary source whether it has been enacted as of 30 September 2026.
- Secondary sources published in 2026 conflict. Evetech's 2026 guide says the R500 "threshold" is a myth because couriers clear every parcel through SARS and charge VAT and clearance fees regardless. JLog's calculator page says goods below R500 clear without duty, but its de minimis guide (updated 29 July 2026) lists R500 CIF and notes no recent change to it, while another JLog page says every parcel is assessed. Treat the safe assumption as: **15% VAT and a courier handling fee should be expected on every courier parcel, whatever its value.** I did not find a SARS page that states the position for 2026 directly, so this should be checked with the courier at checkout.
- Postal delivery (SA Post) avoids the courier fee in principle, but Evetech reports 4 to 12 week delays and a R150 fee.
- Shipping-agent alternative: Scott's Shipping (scottshipping.co.za) quotes an all-in price including duty, VAT and door delivery, with 10 to 15 working days from purchase for AliExpress orders.

### Typical delivery time

- AliExpress via agent: 10 to 15 working days (Scott's Shipping).
- Local marketplace listings on Takealot that ship from overseas show "Ships in 14 - 16 work days" or "18 - 20 work days" on the product page.
- Courier direct from LILYGO, Waveshare or M5Stack: not verified. Express couriers commonly take under two weeks, but I did not see a delivery estimate on those stores.

## Best-value options

| Priority | Option | Price | Why |
|---|---|---|---|
| Cheapest in stock locally | DIY Electronics 2.8" CYD (ESP32CYD) | R387.00 incl. (R336.52 ex) | Colour touchscreen, low stock, pay VAT if not VAT-registered |
| Larger screen locally | Communica BMT ESP32 LVGL 3.5" LCD | R525.00 incl. (R456.52 ex) | Larger display for reading at a distance, Samrand collection or courier |
| Lowest price if restocked | Micro Robotics CYD (E32R28T) | R342.70 incl. (R298.00 ex) | Currently no stock |
| Best-supported hardware (import) | DigiKey ZA M5Stack Core2 v1.3 (K010-V13) or Basic Core V2.7 (K001-V27) | R692.32 and R643.91 ex, plus shipping and import VAT | Enclosed housing, battery, well-documented, 94 and 620 in stock |
| Best import value | AliExpress CYD or LILYGO T-Display-S3 | about R210 to R470 before courier fee | Only sensible if buying several or already importing other parts |

A VAT-registered business (Precept Systems) can normally reclaim input VAT, so ex-VAT prices are the fair comparison.

## Sources

- DIY Electronics product pages (URLs in the table), read 30 September 2026
- Micro Robotics category page: https://www.robotics.org.za/index.php?route=product/category&path=636_955
- Communica Shopify search and product endpoints: https://www.communica.co.za/search/suggest.json and product URLs in the table
- Mantech search: https://www.mantech.co.za/Stock.aspx (posted search form)
- Robofactory: https://www.robofactory.co.za/ product pages in the table
- Netram: https://www.netram.co.za/wifi/11055-esp32-cyd-wifi-bluetooth-28-inch-lcd-touch-display.html
- PiShop: https://www.pishop.co.za/store/ product pages in the table
- Takealot search API: https://api.takealot.com/rest/v-1-14-0/searches/products
- Leobot category scan: https://www.leobot.net/category/1065 and subcategories
- DigiKey South Africa catalogue via the local `dk` command (https://www.digikey.co.za/)
- LILYGO store: https://lilygo.cc/products/t-display-s3 and https://lilygo.cc/products/t-display-s3-amoled
- Waveshare: https://www.waveshare.com/esp32-s3-touch-lcd-3.5.htm and sibling pages
- M5Stack store: https://shop.m5stack.com/
- AliExpress CYD price, from search snippets: https://randomnerdtutorials.com/cheap-yellow-display-esp32-2432s028r/ and https://www.atomic14.com/esp32/boards/esp32-2432s028r/
- eBay CYD listing: https://www.ebay.com/itm/197167870931
- SARS media release, changes to customs import system (8 August 2024): https://www.sars.gov.za/media-release/changes-to-customs-import-system/
- Evetech, Import duties on tech in SA (2026): https://www.evetech.co.za/import-duties-tech-south-africa/e/3921
- JLog import duty guide: https://jlog.co.za/import-duties-south-africa-explained/
- JLog de minimis guide (updated 29 July 2026): https://jlog.co.za/guides/de-minimis-values-south-africa/
- Baker McKenzie on phase-out of import VAT relief: https://insightplus.bakermckenzie.com/bm/tax/south-africa-perhaps-all-goods-things-really-do-come-to-an-end-import-vat-relief-on-small-parcels-set-to-be-phased-out-in-law
- VATupdate: https://www.vatupdate.com/2025/09/01/south-africa-to-end-vat-exemption-on-low-value-imports-impacting-ecommerce-and-education/
- Scott's Shipping (AliExpress to South Africa): https://scottshipping.co.za/aliexpress-south-africa/
- Exchange rate: https://open.er-api.com/v6/latest/USD
