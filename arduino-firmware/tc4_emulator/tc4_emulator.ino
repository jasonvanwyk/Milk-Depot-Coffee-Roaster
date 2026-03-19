/*
 * TC4 Protocol Emulator for Artisan - 2-Channel Thermocouple Version
 *
 * Milk Depot Coffee Roaster - Production Firmware
 * Target: Arduino Nano (ATmega328P, USB-C variant)
 *
 * Emulates the TC4 serial protocol for Artisan roasting software.
 * Reads 2 K-type thermocouples via MAX31855 amplifier modules (SPI).
 *
 * Channels:
 *   - Channel 1 (ET): Exhaust/Environment Temperature
 *   - Channel 2 (BT): Bean Temperature
 *   - Channel 3: Unused (reports 0)
 *   - Channel 4: Unused (reports 0)
 *
 * Artisan Configuration:
 *   - Device: ArduinoTC4 (for channels 1+2)
 *   - Port: /dev/ttyACM0 or /dev/ttyUSB0
 *   - Baud: 115200
 *
 * Hardware:
 *   - Arduino Nano (USB-C)
 *   - 2x MAX31855 thermocouple amplifier modules
 *   - 2x Custom K-type probes (GPA Trading, 316L SS)
 *     - BT: 35mm/2.5mm probe
 *     - ET: 50mm/3.0mm probe
 *   - 1.3" SH1106 OLED display (I2C)
 *   - 100nF ceramic decoupling caps on each MAX31855
 *
 * Author: Jason
 * Repository: https://github.com/jasonvanwyk/Milk-Depot-Coffee-Roaster
 */

#include <SPI.h>
#include <Adafruit_MAX31855.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>

// ============================================================================
// CONFIGURATION
// ============================================================================

const unsigned long BAUD_RATE = 115200;

// SPI Pin Definitions (shared bus)
const int PIN_SCK  = 13;   // SPI Clock (shared)
const int PIN_MISO = 12;   // SPI Data Out (shared)

// Chip Select pins (active low)
const int PIN_CS_ET = 10;  // CS for Exhaust Temperature (Channel 1)
const int PIN_CS_BT = 9;   // CS for Bean Temperature (Channel 2)

// OLED Display (1.3" SH1106, I2C)
const int OLED_WIDTH = 128;
const int OLED_HEIGHT = 64;
const int OLED_ADDR = 0x3C;

// Temperature offset calibration (adjust after calibration)
float calibOffset_ET = 0.0;
float calibOffset_BT = 0.0;

// ============================================================================
// GLOBAL VARIABLES
// ============================================================================

String inputBuffer = "";

float lastTemp_ET = 0.0;
float lastTemp_BT = 0.0;
float ambientTemp = 25.0;

bool error_ET = false;
bool error_BT = false;

bool useFahrenheit = false;
bool oledReady = false;

// ============================================================================
// HARDWARE OBJECTS
// ============================================================================

// MAX31855 using software SPI (flexible pin assignment)
Adafruit_MAX31855 thermoET(PIN_SCK, PIN_CS_ET, PIN_MISO);
Adafruit_MAX31855 thermoBT(PIN_SCK, PIN_CS_BT, PIN_MISO);

// SH1106 OLED display
Adafruit_SH1106G display(OLED_WIDTH, OLED_HEIGHT, &Wire, -1);

// ============================================================================
// SETUP
// ============================================================================

void setup() {
  Serial.begin(BAUD_RATE);

  // Initialize MAX31855 modules
  if (!thermoET.begin()) { error_ET = true; }
  if (!thermoBT.begin()) { error_BT = true; }

  // Initialize OLED display
  if (display.begin(OLED_ADDR, true)) {
    oledReady = true;
    display.clearDisplay();
    display.display();           // flush zeros to display RAM
    delay(100);                  // let the controller settle
    display.setTextSize(1);
    display.setTextColor(SH110X_WHITE);
    display.setCursor(0, 0);
    display.println(F("Milk Depot Roaster"));
    display.println(F("2-Channel TC4"));
    display.println();
    display.println(F("Waiting for Artisan"));
    display.display();
  }

  // Startup message (comment lines ignored by Artisan)
  Serial.println(F("# Milk Depot Coffee Roaster"));
  Serial.println(F("# TC4 Emulator - 2 Channel"));
  Serial.println(F("# Channels: ET, BT"));
  Serial.println(F("# Baud: 115200"));
  Serial.print(F("# ET init: "));
  Serial.println(error_ET ? F("FAIL") : F("OK"));
  Serial.print(F("# BT init: "));
  Serial.println(error_BT ? F("FAIL") : F("OK"));
  Serial.print(F("# OLED: "));
  Serial.println(oledReady ? F("OK") : F("FAIL"));
}

// ============================================================================
// MAIN LOOP
// ============================================================================

void loop() {
  while (Serial.available() > 0) {
    char c = Serial.read();

    if (c == '\n' || c == '\r') {
      if (inputBuffer.length() > 0) {
        handleCommand(inputBuffer);
        inputBuffer = "";
      }
    } else {
      inputBuffer += c;
    }
  }
}

// ============================================================================
// COMMAND HANDLER
// ============================================================================

void handleCommand(String cmd) {
  cmd.toUpperCase();
  cmd.trim();

  if (cmd.startsWith("READ")) {
    sendTemperatures();
  }
  else if (cmd.startsWith("DIAG")) {
    // Raw diagnostic: read 32-bit SPI data from each module
    Serial.print(F("# ET internal: "));
    Serial.println(thermoET.readInternal(), 2);
    Serial.print(F("# ET celsius: "));
    Serial.println(thermoET.readCelsius(), 2);
    Serial.print(F("# ET error: "));
    Serial.println(thermoET.readError());
    Serial.println();
    Serial.print(F("# BT internal: "));
    Serial.println(thermoBT.readInternal(), 2);
    Serial.print(F("# BT celsius: "));
    Serial.println(thermoBT.readCelsius(), 2);
    Serial.print(F("# BT error: "));
    Serial.println(thermoBT.readError());
  }
  else if (cmd.startsWith("CHAN")) {
    Serial.println(F("# CHAN: 1200 (ET, BT, unused, unused)"));
  }
  else if (cmd.startsWith("UNITS")) {
    if (cmd.indexOf('F') >= 0) {
      useFahrenheit = true;
      Serial.println(F("# Units: Fahrenheit"));
    } else {
      useFahrenheit = false;
      Serial.println(F("# Units: Celsius"));
    }
  }
  else if (cmd.startsWith("FILT")) {
    Serial.println(F("# FILT: acknowledged"));
  }
  else if (cmd.startsWith("OT1") || cmd.startsWith("OT2")) {
    // No outputs to control
  }
  else if (cmd.startsWith("IO3")) {
    // Acknowledge
  }
  else if (cmd.startsWith("PID")) {
    Serial.println(F("# PID: acknowledged"));
  }
}

// ============================================================================
// TEMPERATURE READING
// ============================================================================

void sendTemperatures() {
  float tempET = readTemperature_ET();
  float tempBT = readTemperature_BT();

  // Read ambient from ET module's cold junction
  float amb = thermoET.readInternal();
  if (!isnan(amb)) {
    ambientTemp = amb;
  }

  lastTemp_ET = tempET;
  lastTemp_BT = tempBT;

  if (useFahrenheit) {
    tempET = celsiusToFahrenheit(tempET);
    tempBT = celsiusToFahrenheit(tempBT);
  }

  // TC4 response: ambient,chan1,chan2,chan3,chan4
  Serial.print(ambientTemp, 2);
  Serial.print(",");
  Serial.print(tempET, 2);      // Channel 1 = ET
  Serial.print(",");
  Serial.print(tempBT, 2);      // Channel 2 = BT
  Serial.print(",");
  Serial.print("0.00");         // Channel 3 = unused
  Serial.print(",");
  Serial.println("0.00");       // Channel 4 = unused

  updateDisplay();
}

float readTemperature_ET() {
  float temp = thermoET.readCelsius();
  uint8_t err = thermoET.readError();
  if (isnan(temp)) {
    error_ET = true;
    Serial.print(F("# ET err: "));
    if (err & 0x01) Serial.print(F("OPEN "));
    if (err & 0x02) Serial.print(F("SHORT_GND "));
    if (err & 0x04) Serial.print(F("SHORT_VCC "));
    if (err == 0) Serial.print(F("NaN_NO_ERR_BITS "));
    Serial.println();
    return lastTemp_ET;
  }
  error_ET = false;
  return temp + calibOffset_ET;
}

float readTemperature_BT() {
  float temp = thermoBT.readCelsius();
  uint8_t err = thermoBT.readError();
  if (isnan(temp)) {
    error_BT = true;
    Serial.print(F("# BT err: "));
    if (err & 0x01) Serial.print(F("OPEN "));
    if (err & 0x02) Serial.print(F("SHORT_GND "));
    if (err & 0x04) Serial.print(F("SHORT_VCC "));
    if (err == 0) Serial.print(F("NaN_NO_ERR_BITS "));
    Serial.println();
    return lastTemp_BT;
  }
  error_BT = false;
  return temp + calibOffset_BT;
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

float celsiusToFahrenheit(float celsius) {
  return (celsius * 9.0 / 5.0) + 32.0;
}

// ============================================================================
// OLED DISPLAY
// ============================================================================

void updateDisplay() {
  if (!oledReady) return;

  display.clearDisplay();
  display.setTextSize(1);
  display.setCursor(0, 0);

  display.println(F("MILK DEPOT ROASTER"));
  display.println(F("------------------"));
  display.println();

  // ET reading
  display.print(F("ET: "));
  if (error_ET) {
    display.println(F("--- ERR"));
  } else {
    display.print(lastTemp_ET, 1);
    display.println(F(" C"));
  }

  // BT reading
  display.print(F("BT: "));
  if (error_BT) {
    display.println(F("--- ERR"));
  } else {
    display.print(lastTemp_BT, 1);
    display.println(F(" C"));
  }

  display.println();
  display.print(F("Amb: "));
  display.print(ambientTemp, 1);
  display.println(F(" C"));

  display.display();
}
