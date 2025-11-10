// Simple serial test sketch
void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ; // Wait for serial port to connect
  }
  delay(1000);  // Extra delay after serial connects
}

void loop() {
  Serial.println("Hello from Arduino!");
  delay(1000);
}
