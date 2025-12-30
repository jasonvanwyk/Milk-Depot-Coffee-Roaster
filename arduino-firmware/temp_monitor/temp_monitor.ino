/*
 * Milk Depot Coffee Roaster - Temperature Monitor (3-Channel)
 *
 * Continuous output firmware for reading three temperature probes:
 *   - ET (Exhaust/Environment Temperature)
 *   - BT (Bean Temperature)
 *   - FT (Flame Temperature)
 *
 * Sends temperature data over serial in a simple comma-separated format.
 * For use with External Program device type in Artisan or custom parsers.
 *
 * For TC4 protocol compatibility (ArduinoTC4 device type), use tc4_emulator instead.
 *
 * Hardware:
 *   - 3x MAX31855 thermocouple amplifier modules (SPI)
 *   - 3x Olimex TC-K-TYPE-1.5M K-type thermocouples
 *
 * Author: Jason
 * Repository: https://github.com/jasonvanwyk/Milk-Depot-Coffee-Roaster
 */

#include <SPI.h>

// Uncomment when MAX31855 library is installed:
// #include <Adafruit_MAX31855.h>

// ============================================================================
// CONFIGURATION
// ============================================================================

const unsigned long BAUD_RATE = 115200;
const unsigned long SAMPLE_INTERVAL_MS = 1000;  // Send data every 1 second

// SPI Pin Definitions (shared bus)
const int PIN_SCK  = 13;   // SPI Clock (shared)
const int PIN_MISO = 12;   // SPI Data Out (shared)

// Chip Select pins (directly controlled, active low)
const int PIN_CS_ET = 10;  // CS for Exhaust Temperature
const int PIN_CS_BT = 9;   // CS for Bean Temperature
const int PIN_CS_FT = 8;   // CS for Flame Temperature

// Temperature offset calibration (adjust after calibration)
float calibOffset_ET = 0.0;
float calibOffset_BT = 0.0;
float calibOffset_FT = 0.0;

// ============================================================================
// MAX31855 OBJECTS (uncomment when library installed)
// ============================================================================

// Adafruit_MAX31855 thermoET(PIN_SCK, PIN_CS_ET, PIN_MISO);
// Adafruit_MAX31855 thermoBT(PIN_SCK, PIN_CS_BT, PIN_MISO);
// Adafruit_MAX31855 thermoFT(PIN_SCK, PIN_CS_FT, PIN_MISO);

// ============================================================================
// GLOBAL VARIABLES
// ============================================================================

unsigned long lastSampleTime = 0;

// Last good readings (returned on error)
float lastTemp_ET = 0.0;
float lastTemp_BT = 0.0;
float lastTemp_FT = 0.0;

// ============================================================================
// SETUP
// ============================================================================

void setup() {
  Serial.begin(BAUD_RATE);

  // Wait for serial port to connect (needed for some boards)
  while (!Serial) {
    ;
  }

  // Configure CS pins as outputs
  pinMode(PIN_CS_ET, OUTPUT);
  pinMode(PIN_CS_BT, OUTPUT);
  pinMode(PIN_CS_FT, OUTPUT);

  // Deselect all MAX31855 modules
  digitalWrite(PIN_CS_ET, HIGH);
  digitalWrite(PIN_CS_BT, HIGH);
  digitalWrite(PIN_CS_FT, HIGH);

  // Initialize SPI
  SPI.begin();

  // Send startup message
  Serial.println(F("# Milk Depot Coffee Roaster - 3 Channel Temperature Monitor"));
  Serial.println(F("# Format: ET:xxx.x,BT:xxx.x,FT:xxx.x"));
  Serial.println(F("# Baud: 115200, Interval: 1000ms"));
}

// ============================================================================
// MAIN LOOP
// ============================================================================

void loop() {
  unsigned long currentTime = millis();

  if (currentTime - lastSampleTime >= SAMPLE_INTERVAL_MS) {
    lastSampleTime = currentTime;

    // Read all temperatures
    float tempET = readTemperature_ET();
    float tempBT = readTemperature_BT();
    float tempFT = readTemperature_FT();

    // Store last good readings
    lastTemp_ET = tempET;
    lastTemp_BT = tempBT;
    lastTemp_FT = tempFT;

    // Output format: ET:xxx.x,BT:xxx.x,FT:xxx.x
    Serial.print(F("ET:"));
    Serial.print(tempET, 1);
    Serial.print(F(",BT:"));
    Serial.print(tempBT, 1);
    Serial.print(F(",FT:"));
    Serial.println(tempFT, 1);
  }
}

// ============================================================================
// TEMPERATURE READING FUNCTIONS
// ============================================================================

float readTemperature_ET() {
  // WITH MAX31855 LIBRARY (uncomment when hardware connected):
  // float temp = thermoET.readCelsius();
  // if (isnan(temp)) return lastTemp_ET;
  // return temp + calibOffset_ET;

  // SIMULATION MODE:
  return readAnalogSimulated(A0);
}

float readTemperature_BT() {
  // WITH MAX31855 LIBRARY:
  // float temp = thermoBT.readCelsius();
  // if (isnan(temp)) return lastTemp_BT;
  // return temp + calibOffset_BT;

  // SIMULATION MODE:
  return readAnalogSimulated(A1);
}

float readTemperature_FT() {
  // WITH MAX31855 LIBRARY:
  // float temp = thermoFT.readCelsius();
  // if (isnan(temp)) return lastTemp_FT;
  // return temp + calibOffset_FT;

  // SIMULATION MODE:
  return readAnalogSimulated(A2);
}

// Simulated reading from analog noise (for testing without hardware)
float readAnalogSimulated(int analogPin) {
  int raw = analogRead(analogPin);
  float voltage = raw * (5.0 / 1023.0);
  return voltage * 50.0;  // ~0-250C range
}

// ============================================================================
// HARDWARE ACTIVATION INSTRUCTIONS
// ============================================================================

/*
 * TO ENABLE MAX31855 THERMOCOUPLES:
 *
 * 1. Install Adafruit MAX31855 library via Arduino IDE Library Manager
 *
 * 2. Uncomment: #include <Adafruit_MAX31855.h>
 *
 * 3. Uncomment the thermocouple object declarations
 *
 * 4. In each readTemperature_XX function:
 *    - Uncomment the MAX31855 code block
 *    - Comment out/delete the readAnalogSimulated() call
 *
 * 5. Compile and upload
 *
 * WIRING:
 *   MAX31855 modules share SCK (D13) and MISO (D12)
 *   Each has unique CS: ET->D10, BT->D9, FT->D8
 *   All powered from 5V and GND
 */
