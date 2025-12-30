/*
 * TC4 Protocol Emulator for Artisan - 3-Channel Thermocouple Version
 *
 * Milk Depot Coffee Roaster - Production Firmware
 *
 * Emulates the TC4 serial protocol for Artisan roasting software.
 * Reads 3 K-type thermocouples via MAX31855 amplifier modules (SPI).
 *
 * Channels:
 *   - Channel 1 (ET): Exhaust/Environment Temperature
 *   - Channel 2 (BT): Bean Temperature
 *   - Channel 3 (FT): Flame/Burner Temperature
 *   - Channel 4: Unused (reports 0)
 *
 * Artisan Configuration:
 *   - Device: ArduinoTC4 (for channels 1+2)
 *   - Extra Device: ArduinoTC4_34 (for channels 3+4)
 *   - Port: /dev/ttyACM0
 *   - Baud: 115200
 *
 * Hardware:
 *   - 3x MAX31855 thermocouple amplifier modules
 *   - 3x Olimex TC-K-TYPE-1.5M K-type thermocouples
 *   - Optional: SSD1306 OLED display for local readout
 *
 * Author: Jason
 * Repository: https://github.com/jasonvanwyk/Milk-Depot-Coffee-Roaster
 */

#include <SPI.h>

// Uncomment when MAX31855 library is installed:
// #include <Adafruit_MAX31855.h>

// Uncomment for OLED display support:
// #include <Wire.h>
// #include <Adafruit_GFX.h>
// #include <Adafruit_SSD1306.h>

// ============================================================================
// CONFIGURATION
// ============================================================================

const unsigned long BAUD_RATE = 115200;

// SPI Pin Definitions (shared bus)
const int PIN_SCK  = 13;   // SPI Clock (shared)
const int PIN_MISO = 12;   // SPI Data Out (shared, directly with MAX31855 DO)

// Chip Select pins (directly controlled, active low)
// Using direct GPIO bitbanging instead of hardware SPI for flexibility
const int PIN_CS_ET = 10;  // CS for Exhaust Temperature (Channel 1)
const int PIN_CS_BT = 9;   // CS for Bean Temperature (Channel 2)
const int PIN_CS_FT = 8;   // CS for Flame Temperature (Channel 3)

// OLED Display (optional)
// const int OLED_WIDTH = 128;
// const int OLED_HEIGHT = 64;
// const int OLED_ADDR = 0x3C;

// Temperature offset calibration (adjust after calibration)
float calibOffset_ET = 0.0;
float calibOffset_BT = 0.0;
float calibOffset_FT = 0.0;

// Simulated ambient temperature (from onboard sensor or fixed)
const float AMBIENT_TEMP = 25.0;

// ============================================================================
// GLOBAL VARIABLES
// ============================================================================

// Serial input buffer for command parsing
String inputBuffer = "";

// Last temperature readings (for display/debugging)
float lastTemp_ET = 0.0;
float lastTemp_BT = 0.0;
float lastTemp_FT = 0.0;

// Error flags
bool error_ET = false;
bool error_BT = false;
bool error_FT = false;

// Units (C or F)
bool useFahrenheit = false;

// ============================================================================
// MAX31855 OBJECTS (uncomment when library installed)
// ============================================================================

// Using software SPI for flexibility with multiple CS pins
// Adafruit_MAX31855 thermoET(PIN_SCK, PIN_CS_ET, PIN_MISO);
// Adafruit_MAX31855 thermoBT(PIN_SCK, PIN_CS_BT, PIN_MISO);
// Adafruit_MAX31855 thermoFT(PIN_SCK, PIN_CS_FT, PIN_MISO);

// ============================================================================
// OLED DISPLAY (uncomment when library installed)
// ============================================================================

// Adafruit_SSD1306 display(OLED_WIDTH, OLED_HEIGHT, &Wire, -1);

// ============================================================================
// SETUP
// ============================================================================

void setup() {
  Serial.begin(BAUD_RATE);

  // Configure CS pins as outputs
  pinMode(PIN_CS_ET, OUTPUT);
  pinMode(PIN_CS_BT, OUTPUT);
  pinMode(PIN_CS_FT, OUTPUT);

  // Deselect all MAX31855 modules (CS high = inactive)
  digitalWrite(PIN_CS_ET, HIGH);
  digitalWrite(PIN_CS_BT, HIGH);
  digitalWrite(PIN_CS_FT, HIGH);

  // Initialize SPI
  SPI.begin();

  // Initialize MAX31855 modules (uncomment when library installed)
  // Note: Adafruit library handles SPI initialization internally
  // if (!thermoET.begin()) { error_ET = true; }
  // if (!thermoBT.begin()) { error_BT = true; }
  // if (!thermoFT.begin()) { error_FT = true; }

  // Initialize OLED display (uncomment when library installed)
  // if (display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
  //   display.clearDisplay();
  //   display.setTextSize(1);
  //   display.setTextColor(SSD1306_WHITE);
  //   display.setCursor(0, 0);
  //   display.println(F("Milk Depot Roaster"));
  //   display.println(F("3-Channel TC4"));
  //   display.display();
  //   delay(1000);
  // }

  // Send startup message (comment lines ignored by Artisan)
  Serial.println(F("# Milk Depot Coffee Roaster"));
  Serial.println(F("# TC4 Emulator - 3 Channel"));
  Serial.println(F("# Channels: ET, BT, FT"));
  Serial.println(F("# Baud: 115200"));
}

// ============================================================================
// MAIN LOOP
// ============================================================================

void loop() {
  // Process incoming serial commands from Artisan
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

  // READ - Main temperature query command
  if (cmd.startsWith("READ")) {
    sendTemperatures();
  }
  // CHAN - Channel mapping configuration
  else if (cmd.startsWith("CHAN")) {
    // CHAN;ijkl sets which physical channels map to logical channels
    // We support 1,2,3 (ET, BT, FT)
    Serial.println(F("# CHAN: 1230 (ET, BT, FT, unused)"));
  }
  // UNITS - Temperature units (C or F)
  else if (cmd.startsWith("UNITS")) {
    if (cmd.indexOf('F') >= 0) {
      useFahrenheit = true;
      Serial.println(F("# Units: Fahrenheit"));
    } else {
      useFahrenheit = false;
      Serial.println(F("# Units: Celsius"));
    }
  }
  // FILT - Filter/smoothing settings
  else if (cmd.startsWith("FILT")) {
    Serial.println(F("# FILT: acknowledged"));
  }
  // OT1/OT2 - Output commands (heater/fan control)
  else if (cmd.startsWith("OT1") || cmd.startsWith("OT2")) {
    // Acknowledge but no actual outputs to control
    // Future: could control relays for heater/fan
  }
  // IO3 - I/O command
  else if (cmd.startsWith("IO3")) {
    // Acknowledge
  }
  // PID - PID control commands
  else if (cmd.startsWith("PID")) {
    Serial.println(F("# PID: acknowledged"));
  }
  // Unknown commands - ignore silently
}

// ============================================================================
// TEMPERATURE READING
// ============================================================================

void sendTemperatures() {
  // Read all three thermocouples
  float tempET = readTemperature_ET();
  float tempBT = readTemperature_BT();
  float tempFT = readTemperature_FT();

  // Store for display
  lastTemp_ET = tempET;
  lastTemp_BT = tempBT;
  lastTemp_FT = tempFT;

  // Convert to Fahrenheit if requested
  if (useFahrenheit) {
    tempET = celsiusToFahrenheit(tempET);
    tempBT = celsiusToFahrenheit(tempBT);
    tempFT = celsiusToFahrenheit(tempFT);
  }

  // TC4 response format: ambient,chan1,chan2,chan3,chan4
  // Artisan ArduinoTC4 maps: Chan1->ET, Chan2->BT
  // ArduinoTC4_34 extra device maps: Chan3->extra1, Chan4->extra2
  Serial.print(AMBIENT_TEMP, 2);
  Serial.print(",");
  Serial.print(tempET, 2);      // Channel 1 = ET (Exhaust)
  Serial.print(",");
  Serial.print(tempBT, 2);      // Channel 2 = BT (Bean)
  Serial.print(",");
  Serial.print(tempFT, 2);      // Channel 3 = FT (Flame)
  Serial.print(",");
  Serial.println("0.00");       // Channel 4 = unused

  // Update OLED display (uncomment when enabled)
  // updateDisplay();
}

// Read Exhaust Temperature (Channel 1)
float readTemperature_ET() {
  // WITH MAX31855 LIBRARY (uncomment when hardware connected):
  // float temp = thermoET.readCelsius();
  // if (isnan(temp)) {
  //   error_ET = true;
  //   return lastTemp_ET;  // Return last good reading on error
  // }
  // error_ET = false;
  // return temp + calibOffset_ET;

  // SIMULATION MODE (remove when hardware connected):
  return readAnalogSimulated(PIN_CS_ET);
}

// Read Bean Temperature (Channel 2)
float readTemperature_BT() {
  // WITH MAX31855 LIBRARY (uncomment when hardware connected):
  // float temp = thermoBT.readCelsius();
  // if (isnan(temp)) {
  //   error_BT = true;
  //   return lastTemp_BT;
  // }
  // error_BT = false;
  // return temp + calibOffset_BT;

  // SIMULATION MODE (remove when hardware connected):
  return readAnalogSimulated(PIN_CS_BT);
}

// Read Flame Temperature (Channel 3)
float readTemperature_FT() {
  // WITH MAX31855 LIBRARY (uncomment when hardware connected):
  // float temp = thermoFT.readCelsius();
  // if (isnan(temp)) {
  //   error_FT = true;
  //   return lastTemp_FT;
  // }
  // error_FT = false;
  // return temp + calibOffset_FT;

  // SIMULATION MODE (remove when hardware connected):
  return readAnalogSimulated(PIN_CS_FT);
}

// Simulated temperature reading from analog noise (for testing without hardware)
float readAnalogSimulated(int pin) {
  // Use the CS pin number as analog input for simulation
  int analogPin = A0;
  if (pin == PIN_CS_BT) analogPin = A1;
  if (pin == PIN_CS_FT) analogPin = A2;

  int raw = analogRead(analogPin);
  float voltage = raw * (5.0 / 1023.0);
  return voltage * 50.0;  // ~0-250C range from noise
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

float celsiusToFahrenheit(float celsius) {
  return (celsius * 9.0 / 5.0) + 32.0;
}

// ============================================================================
// OLED DISPLAY UPDATE (uncomment when library installed)
// ============================================================================

/*
void updateDisplay() {
  display.clearDisplay();
  display.setTextSize(1);
  display.setCursor(0, 0);

  // Header
  display.println(F("MILK DEPOT ROASTER"));
  display.println(F("------------------"));

  // Temperature readings
  display.setTextSize(1);

  display.print(F("ET: "));
  display.print(lastTemp_ET, 1);
  display.print(F("C"));
  if (error_ET) display.print(F(" ERR"));
  display.println();

  display.print(F("BT: "));
  display.print(lastTemp_BT, 1);
  display.print(F("C"));
  if (error_BT) display.print(F(" ERR"));
  display.println();

  display.print(F("FT: "));
  display.print(lastTemp_FT, 1);
  display.print(F("C"));
  if (error_FT) display.print(F(" ERR"));
  display.println();

  display.display();
}
*/

// ============================================================================
// HARDWARE ACTIVATION INSTRUCTIONS
// ============================================================================

/*
 * TO ENABLE MAX31855 THERMOCOUPLES:
 *
 * 1. Install Adafruit MAX31855 library:
 *    - Arduino IDE: Sketch -> Include Library -> Manage Libraries
 *    - Search "Adafruit MAX31855" and install
 *    - Also install "Adafruit BusIO" if prompted
 *
 * 2. Uncomment these lines at top of file:
 *    #include <Adafruit_MAX31855.h>
 *
 * 3. Uncomment the thermocouple object declarations:
 *    Adafruit_MAX31855 thermoET(PIN_SCK, PIN_CS_ET, PIN_MISO);
 *    Adafruit_MAX31855 thermoBT(PIN_SCK, PIN_CS_BT, PIN_MISO);
 *    Adafruit_MAX31855 thermoFT(PIN_SCK, PIN_CS_FT, PIN_MISO);
 *
 * 4. In readTemperature_ET/BT/FT functions:
 *    - Uncomment the MAX31855 library code block
 *    - Delete or comment out the readAnalogSimulated() call
 *
 * 5. Compile and upload
 *
 * TO ENABLE OLED DISPLAY:
 *
 * 1. Install libraries:
 *    - Adafruit SSD1306
 *    - Adafruit GFX Library
 *
 * 2. Uncomment the #include lines for Wire, GFX, and SSD1306
 *
 * 3. Uncomment display object and initialization in setup()
 *
 * 4. Uncomment updateDisplay() function and call in sendTemperatures()
 *
 * WIRING:
 *
 * MAX31855 modules (all share SCK and MISO):
 *   - VCC -> 5V
 *   - GND -> GND
 *   - SCK -> D13 (shared)
 *   - DO  -> D12 (shared, directly connected is OK)
 *   - CS (ET) -> D10
 *   - CS (BT) -> D9
 *   - CS (FT) -> D8
 *
 * OLED Display (I2C):
 *   - VCC -> 5V (or 3.3V)
 *   - GND -> GND
 *   - SDA -> A4
 *   - SCL -> A5
 *
 * CALIBRATION:
 *
 * 1. Place all probes in ice water bath (0°C)
 * 2. Note the readings for each channel
 * 3. Set calibOffset_XX = 0.0 - reading
 *    Example: if ET reads 2.3°C in ice water, set calibOffset_ET = -2.3
 *
 * 4. Verify with boiling water (100°C at sea level)
 */
