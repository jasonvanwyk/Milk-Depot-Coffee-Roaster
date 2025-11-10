/*
 * Milk Depot Coffee Roaster - Temperature Monitor
 *
 * Arduino firmware for reading two temperature probes:
 * - Bean Temperature (BT)
 * - Drum Temperature (DT)
 *
 * Sends temperature data over serial to Artisan software running on Raspberry Pi
 *
 * Author: Jason
 * Repository: https://github.com/jasonvanwyk/Milk-Depot-Coffee-Roaster
 * License: MIT
 */

// Configuration
const unsigned long BAUD_RATE = 115200;
const unsigned long SAMPLE_INTERVAL_MS = 1000;  // Send data every 1 second

// Temperature probe pins
// NOTE: Adjust these based on your actual hardware connections
const int BEAN_TEMP_PIN = A0;    // Bean temperature probe (analog pin)
const int DRUM_TEMP_PIN = A1;    // Drum temperature probe (analog pin)

// Calibration constants (adjust based on your probes)
// For K-type thermocouples with amplifier modules (like MAX6675 or MAX31855)
// These are placeholder values - you'll need to calibrate
const float BEAN_TEMP_OFFSET = 0.0;   // Offset in degrees Celsius
const float BEAN_TEMP_SCALE = 1.0;    // Scale factor
const float DRUM_TEMP_OFFSET = 0.0;   // Offset in degrees Celsius
const float DRUM_TEMP_SCALE = 1.0;    // Scale factor

// If using MAX6675 or MAX31855 thermocouple amplifier modules:
// Uncomment the appropriate library and update the pin definitions
// #include <max6675.h>
// MAX6675 beanThermocouple(thermoDO, thermoCS_bean, thermoCLK);
// MAX6675 drumThermocouple(thermoDO, thermoCS_drum, thermoCLK);

// Timing
unsigned long lastSampleTime = 0;

void setup() {
  // Initialize serial communication
  Serial.begin(BAUD_RATE);

  // Wait for serial port to connect (needed for some boards)
  while (!Serial) {
    ; // Wait for serial port to connect
  }

  // Initialize analog pins (if using direct analog readings)
  pinMode(BEAN_TEMP_PIN, INPUT);
  pinMode(DRUM_TEMP_PIN, INPUT);

  // Send startup message
  Serial.println("# Milk Depot Coffee Roaster - Temperature Monitor");
  Serial.println("# Ready to send temperature data");
  Serial.println("# Format: BT:xxx.x,DT:xxx.x");
}

void loop() {
  unsigned long currentTime = millis();

  // Check if it's time to take a sample
  if (currentTime - lastSampleTime >= SAMPLE_INTERVAL_MS) {
    lastSampleTime = currentTime;

    // Read temperatures
    float beanTemp = readBeanTemperature();
    float drumTemp = readDrumTemperature();

    // Send data in Artisan-compatible format
    // Format: BT:xxx.x,DT:xxx.x\n
    Serial.print("BT:");
    Serial.print(beanTemp, 1);  // 1 decimal place
    Serial.print(",DT:");
    Serial.print(drumTemp, 1);  // 1 decimal place
    Serial.println();
  }
}

// Read bean temperature probe
float readBeanTemperature() {
  // OPTION 1: Using MAX6675/MAX31855 library
  // Uncomment if using thermocouple amplifier module
  // return beanThermocouple.readCelsius();

  // OPTION 2: Direct analog reading (for basic thermistors or voltage output sensors)
  int rawValue = analogRead(BEAN_TEMP_PIN);

  // Convert analog reading to temperature
  // This conversion depends on your specific sensor
  // Example for 10-bit ADC (0-1023) with 5V reference and linear sensor:
  float voltage = rawValue * (5.0 / 1023.0);

  // Example conversion (adjust for your sensor):
  // Many analog temp sensors output 10mV per degree Celsius
  // float tempC = voltage * 100.0;

  // Placeholder: Replace with your actual conversion formula
  float tempC = voltage * 50.0;  // Example scaling

  // Apply calibration
  tempC = (tempC * BEAN_TEMP_SCALE) + BEAN_TEMP_OFFSET;

  return tempC;
}

// Read drum temperature probe
float readDrumTemperature() {
  // OPTION 1: Using MAX6675/MAX31855 library
  // Uncomment if using thermocouple amplifier module
  // return drumThermocouple.readCelsius();

  // OPTION 2: Direct analog reading (for basic thermistors or voltage output sensors)
  int rawValue = analogRead(DRUM_TEMP_PIN);

  // Convert analog reading to temperature
  float voltage = rawValue * (5.0 / 1023.0);

  // Placeholder: Replace with your actual conversion formula
  float tempC = voltage * 50.0;  // Example scaling

  // Apply calibration
  tempC = (tempC * DRUM_TEMP_SCALE) + DRUM_TEMP_OFFSET;

  return tempC;
}

/*
 * HARDWARE SETUP NOTES:
 *
 * For K-type thermocouples with MAX6675 or MAX31855 modules:
 * 1. Install the appropriate library via Arduino IDE Library Manager:
 *    - Search for "MAX6675" or "MAX31855"
 *    - Install the Adafruit library
 *
 * 2. Wiring for MAX6675/MAX31855 (SPI interface):
 *    - VCC -> 5V (or 3.3V depending on module)
 *    - GND -> GND
 *    - SCK (Clock) -> Digital pin (e.g., D13 on Uno)
 *    - SO (Data Out) -> Digital pin (e.g., D12 on Uno)
 *    - CS (Chip Select) -> Digital pin (unique for each sensor)
 *
 * 3. Update the code to use thermocouple libraries (see commented sections)
 *
 * For analog thermistors or voltage-output sensors:
 * 1. Connect sensor output to analog pins (A0, A1)
 * 2. Update the conversion formulas based on sensor datasheet
 * 3. Calibrate using known temperature references (ice water, boiling water)
 *
 * CALIBRATION PROCEDURE:
 * 1. Place both probes in ice water (0°C) and note the readings
 * 2. Place both probes in boiling water (100°C) and note the readings
 * 3. Calculate offset and scale factors:
 *    offset = 0 - reading_at_0C
 *    scale = 100 / (reading_at_100C - reading_at_0C)
 * 4. Update BEAN_TEMP_OFFSET, BEAN_TEMP_SCALE, etc.
 */
