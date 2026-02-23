# Arduino CLI Workflow

Complete guide for using Arduino CLI to develop and upload firmware from the Raspberry Pi.

## Overview

Arduino CLI is installed locally in this project at `/home/jason/artisan/bin/arduino-cli`. This allows direct communication with the Arduino from the Raspberry Pi without needing a separate computer.

## Installation Details

- **Version**: 1.3.1
- **Location**: `/home/jason/artisan/bin/arduino-cli`
- **Config**: `~/.arduino15/arduino-cli.yaml`
- **Cores Installed**: arduino:avr@1.8.6 (for Arduino UNO R3)
- **Libraries Installed**:
  - Adafruit MAX31855 library v1.4.2
  - Adafruit BusIO v1.17.4
  - LiquidCrystal v1.0.7

## Quick Start

### 1. Detect Arduino

```bash
cd /home/jason/artisan
./scripts/detect.sh
```

This will show connected Arduino boards and serial ports.

### 2. Compile Firmware

```bash
./scripts/compile.sh
```

Or compile a specific sketch:
```bash
./scripts/compile.sh arduino-firmware/serial_test
```

### 3. Upload to Arduino

```bash
./scripts/upload.sh
```

Or specify port and sketch:
```bash
./scripts/upload.sh arduino-firmware/temp_monitor /dev/ttyACM0
```

### 4. Monitor Serial Output

```bash
./scripts/monitor.sh
```

This runs the Python serial monitor script.

## Manual Commands

If you prefer to use arduino-cli directly:

```bash
# Add to PATH first
export PATH="/home/jason/artisan/bin:$PATH"

# List connected boards
arduino-cli board list

# Compile
arduino-cli compile --fqbn arduino:avr:uno arduino-firmware/temp_monitor/

# Upload
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno arduino-firmware/temp_monitor/

# Monitor serial
arduino-cli monitor -p /dev/ttyACM0 -c baudrate=115200
```

## Available Sketches

### 1. temp_monitor (Main Project)
**Location**: `arduino-firmware/temp_monitor/`

Production firmware for reading two temperature probes.

**Features**:
- Reads bean temperature (BT) and drum temperature (DT)
- Sends data at 115200 baud
- Format: `BT:xxx.x,DT:xxx.x`
- Supports both analog sensors and MAX31855 modules

**To Use**:
```bash
./scripts/compile.sh arduino-firmware/temp_monitor
./scripts/upload.sh arduino-firmware/temp_monitor
./scripts/monitor.sh
```

### 2. serial_test (Diagnostic)
**Location**: `arduino-firmware/serial_test/`

Simple test sketch for verifying serial communication.

**Features**:
- Sends "Hello from Arduino!" every second
- 115200 baud
- Useful for troubleshooting

**To Use**:
```bash
./scripts/compile.sh arduino-firmware/serial_test
./scripts/upload.sh arduino-firmware/serial_test
./scripts/monitor.sh
```

## Troubleshooting

### Arduino Not Detected

**Symptom**: `arduino-cli board list` shows "No boards found"

**Solutions**:
1. **Check Physical Connection**:
   ```bash
   ls -la /dev/ttyACM* /dev/ttyUSB*
   ```
   You should see `/dev/ttyACM0` or similar.

2. **Check USB Messages**:
   ```bash
   dmesg | tail -20
   ```
   Should show Arduino connection messages.

3. **Check Permissions**:
   ```bash
   groups
   ```
   You should be in the `dialout` group (already configured).

4. **Try Different USB Port/Cable**:
   - Try another USB port on the Pi
   - Try a different USB cable (must be data cable, not charge-only)

### Upload Fails - "stk500_getsync()"

**Symptom**: `stk500_getsync() attempt X of 10: not in sync`

**Causes**:
- Arduino is running a sketch that's continuously sending serial data
- Bootloader can't sync because serial port is busy
- Wrong board type selected
- Broken Arduino hardware

**Solutions**:
1. **Press Reset During Upload**:
   - Start the upload command
   - Press the Arduino reset button when you see "Uploading..."
   - This gives the bootloader a clean window to sync

2. **Kill Processes Using Serial Port**:
   ```bash
   lsof /dev/ttyACM0
   # Kill any processes shown
   ```

3. **Try Old Bootloader**:
   ```bash
   arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno:cpu=atmega328old
   ```

4. **Re-burn Bootloader** (requires ISP programmer):
   If Arduino bootloader is corrupted, you'll need an ISP programmer to restore it.

### Garbled Serial Output

**Symptom**: Serial monitor shows garbage characters like `|p��p�p�`

**Causes**:
- Baud rate mismatch
- Broken Arduino UART hardware
- Crystal oscillator issue
- Corrupted firmware

**Solutions**:
1. **Verify Baud Rate**:
   Make sure Arduino code uses `Serial.begin(115200)` and monitor uses 115200 baud.

2. **Try Different Baud Rates**:
   ```bash
   # Test common baud rates
   for baud in 9600 19200 38400 57600 115200; do
     echo "Testing $baud"
     stty -F /dev/ttyACM0 $baud raw -echo
     timeout 2 cat /dev/ttyACM0
   done
   ```

3. **Upload Simple Test Sketch**:
   ```bash
   ./scripts/compile.sh arduino-firmware/serial_test
   ./scripts/upload.sh arduino-firmware/serial_test
   ./scripts/monitor.sh
   ```
   If this also shows garbled output, it's likely hardware.

4. **Test on Different Computer**:
   Upload the same sketch using Arduino IDE on another computer to isolate the issue.

5. **Check Arduino Board**:
   - **Clone Boards**: Some Arduino clones have bad crystals or fake UART chips
   - **Damaged Board**: Physical damage to the board
   - **Bad USB-Serial Chip**: The CH340/CP2102/ATmega16U2 chip might be faulty

**Hardware Diagnosis**:
If output is garbled at ALL baud rates on BOTH simple and complex sketches:
- **Likely Cause**: Broken Arduino board (bad crystal, damaged UART, or defective USB-serial chip)
- **Solution**: Try a different Arduino board

### No Serial Output

**Symptom**: Monitor shows nothing, no data received

**Solutions**:
1. **Wait for Arduino to Boot**:
   Arduino resets when serial connection opens. Wait 2-3 seconds.

2. **Check Firmware is Uploaded**:
   ```bash
   ./scripts/detect.sh
   ```

3. **Verify TX/RX LEDs**:
   The TX/RX LEDs on Arduino should blink when sending data.

4. **Check Code**:
   Ensure `Serial.begin()` is called in `setup()`.

### Library Not Found

**Symptom**: Compilation error about missing library

**Solution**:
```bash
export PATH="/home/jason/artisan/bin:$PATH"

# Search for library
arduino-cli lib search MAX31855

# Install library
arduino-cli lib install "Adafruit MAX31855 library"
```

### Port Access Denied

**Symptom**: `Permission denied` when accessing `/dev/ttyACM0`

**Solution**:
```bash
# Check groups
groups

# If dialout is missing, add yourself
sudo usermod -a -G dialout $USER

# Log out and back in for changes to take effect
```

## Updating Arduino CLI

To update to the latest version:

```bash
cd /home/jason/artisan
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
```

## Adding More Arduino Libraries

```bash
export PATH="/home/jason/artisan/bin:$PATH"

# Search for a library
arduino-cli lib search MAX6675

# Install a library
arduino-cli lib install "MAX6675"

# List installed libraries
arduino-cli lib list
```

## Working with Multiple Arduino Boards

If you have multiple Arduinos connected:

```bash
# List all boards with their ports
arduino-cli board list

# Upload to specific port
./scripts/upload.sh arduino-firmware/temp_monitor /dev/ttyACM1
```

## Configuration

Arduino CLI config file: `~/.arduino15/arduino-cli.yaml`

View config:
```bash
export PATH="/home/jason/artisan/bin:$PATH"
arduino-cli config dump
```

## References

- [Arduino CLI Documentation](https://arduino.github.io/arduino-cli/)
- [Arduino CLI Command Reference](https://arduino.github.io/arduino-cli/commands/arduino-cli/)
- [Arduino Serial Reference](https://www.arduino.cc/reference/en/language/functions/communication/serial/)

## Known Issues

### Current Arduino Hardware Issue

**Date**: 2025-11-10

**Symptom**: Serial output is garbled at all baud rates with patterns like `|p��p�p�`

**Diagnosis**:
- Tested multiple baud rates (9600, 19200, 38400, 57600, 115200)
- Uploaded both simple and complex sketches
- Output remains garbled regardless of configuration
- Upload sometimes succeeds, sometimes fails with sync errors

**Conclusion**: Likely broken Arduino board hardware
- Possible bad crystal oscillator (causing baud rate mismatch)
- Possible damaged UART/USB-serial chip
- Or defective Arduino clone

**Recommendation**: Test with a different Arduino UNO R3 board to verify the issue is hardware-related.

**Workaround**: None - hardware replacement needed if diagnosis is confirmed.

---

**Last Updated**: 2025-11-10
