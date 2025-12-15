/*
 * TC4 Protocol Emulator for Artisan
 * 
 * Emulates the TC4 serial protocol on a plain Arduino (no TC4 shield).
 * Reads analog pins A0 (BT) and A1 (ET) and responds to Artisan commands.
 * 
 * Protocol: Responds to READ command with temperature data
 * Format: ambient,chan1,chan2,chan3,chan4
 * 
 * For use with: Artisan -> Config -> Device -> ArduinoTC4
 * Baud: 115200
 */

const unsigned long BAUD_RATE = 115200;

// Temperature probe pins (analog)
const int BT_PIN = A0;  // Bean Temperature -> Channel 1
const int ET_PIN = A1;  // Environment/Exhaust Temperature -> Channel 2

// Serial input buffer
String inputBuffer = "";

// Simulated ambient temperature
const float AMBIENT_TEMP = 25.0;

void setup() {
  Serial.begin(BAUD_RATE);
  
  pinMode(BT_PIN, INPUT);
  pinMode(ET_PIN, INPUT);
  
  // Send startup message (commented lines are ignored by Artisan)
  Serial.println("# TC4 Emulator Ready");
  Serial.println("# Baud: 115200");
}

void loop() {
  // Check for serial commands from Artisan
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

void handleCommand(String cmd) {
  // Convert to uppercase for comparison
  cmd.toUpperCase();
  cmd.trim();
  
  // Handle READ command - main command Artisan uses
  if (cmd.startsWith("READ")) {
    sendTemperatures();
  }
  // Handle CHAN command - channel mapping
  else if (cmd.startsWith("CHAN")) {
    Serial.println("# Active channels set to 1200");
  }
  // Handle UNITS command
  else if (cmd.startsWith("UNITS")) {
    if (cmd.indexOf('F') >= 0) {
      Serial.println("# Units set to F");
    } else {
      Serial.println("# Units set to C");
    }
  }
  // Handle FILT command - filtering
  else if (cmd.startsWith("FILT")) {
    Serial.println("# Filters set");
  }
  // Handle OT1/OT2 commands - heater/fan control (acknowledge but ignore)
  else if (cmd.startsWith("OT1") || cmd.startsWith("OT2")) {
    // Acknowledge but we have no outputs to control
  }
  // Handle PID commands
  else if (cmd.startsWith("PID")) {
    Serial.println("# PID command received");
  }
  // Unknown command - ignore silently
}

void sendTemperatures() {
  // Read analog values
  int btRaw = analogRead(BT_PIN);
  int etRaw = analogRead(ET_PIN);
  
  // Convert to temperature (placeholder formula)
  // Adjust this based on your actual sensors
  float btTemp = analogToTemp(btRaw);
  float etTemp = analogToTemp(etRaw);
  
  // TC4 response format: ambient,chan1,chan2,chan3,chan4
  // Chan1 = ET (environment/exhaust), Chan2 = BT (bean)
  // Artisan ArduinoTC4 device maps: Chan1->ET, Chan2->BT
  Serial.print(AMBIENT_TEMP, 2);
  Serial.print(",");
  Serial.print(etTemp, 2);      // Channel 1 = ET
  Serial.print(",");
  Serial.print(btTemp, 2);      // Channel 2 = BT
  Serial.print(",");
  Serial.print("0.00");         // Channel 3 = unused
  Serial.print(",");
  Serial.println("0.00");       // Channel 4 = unused
}

float analogToTemp(int raw) {
  // Convert 10-bit ADC reading to temperature
  // This is a placeholder - adjust for your sensors
  // 
  // For testing without sensors: floating pins give ~60-120C noise
  // For PT100 with proper amplifier: use appropriate formula
  // For MAX31855: would use SPI, not analog
  
  float voltage = raw * (5.0 / 1023.0);
  float tempC = voltage * 50.0;  // Simple scaling for testing
  
  return tempC;
}
