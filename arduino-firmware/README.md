# Arduino Temperature Monitor Firmware

Custom Arduino firmware for the Milk Depot Coffee Roaster to read two temperature probes and communicate with Artisan software.

## Overview

This firmware reads temperature from two probes:
- **Bean Temperature (BT)** - Measures the coffee bean temperature during roasting
- **Drum Temperature (DT)** - Measures the roasting drum temperature

Temperature data is sent over USB serial connection to the Raspberry Pi running Artisan software.

## Hardware Requirements

### Required Components
- Arduino UNO R3 (or compatible)
- 2x Temperature probes (K-type thermocouples recommended)
- 2x Thermocouple amplifier modules (MAX6675 or MAX31855)
- USB cable for Arduino → Raspberry Pi connection
- Jumper wires for connections

### Recommended: MAX31855 Thermocouple Modules

The MAX31855 is recommended over MAX6675 because:
- Wider temperature range (-200°C to +1350°C vs 0°C to +1024°C)
- Better accuracy (±2°C vs ±4°C)
- Cold-junction compensation
- 14-bit resolution

## Wiring Diagram

### Using MAX31855 Modules (SPI Interface)

```
Arduino UNO          MAX31855 Module #1 (Bean Temp)
-----------          ---------------------------
5V         --------> VCC
GND        --------> GND
Pin 13(SCK)--------> CLK
Pin 12(MISO)-------> SO
Pin 10(SS) --------> CS

Arduino UNO          MAX31855 Module #2 (Drum Temp)
-----------          ---------------------------
5V         --------> VCC (shared with module #1)
GND        --------> GND (shared with module #1)
Pin 13(SCK)--------> CLK (shared with module #1)
Pin 12(MISO)-------> SO (shared with module #1)
Pin 9(SS)  --------> CS (unique pin for module #2)
```

**Note**: Both modules share the SPI bus (CLK and SO/MISO), but each needs a unique Chip Select (CS) pin.

### Alternative: Analog Temperature Sensors

If using analog sensors (thermistors, LM35, TMP36, etc.):
```
Sensor Output -> Arduino A0 (Bean Temp)
Sensor Output -> Arduino A1 (Drum Temp)
```

You'll need to modify the conversion formulas in the code based on your sensor's datasheet.

## Installation

### 1. Install Required Libraries

If using MAX6675 or MAX31855 modules:

1. Open Arduino IDE
2. Go to **Sketch** → **Include Library** → **Manage Libraries**
3. Search for "MAX31855" (or "MAX6675")
4. Install "Adafruit MAX31855" library

### 2. Modify the Code for Your Hardware

Edit `temp_monitor.ino`:

#### For MAX31855 Modules:

Uncomment and modify the library includes and pin definitions:

```cpp
#include <Adafruit_MAX31855.h>

// Pin definitions
#define MAXDO   12  // Data Out (MISO)
#define MAXCS_BEAN 10  // Chip Select for bean temp
#define MAXCS_DRUM 9   // Chip Select for drum temp
#define MAXCLK  13  // Clock (SCK)

// Initialize thermocouples
Adafruit_MAX31855 beanThermocouple(MAXCLK, MAXCS_BEAN, MAXDO);
Adafruit_MAX31855 drumThermocouple(MAXCLK, MAXCS_DRUM, MAXDO);
```

Then update the temperature reading functions:
```cpp
float readBeanTemperature() {
  return beanThermocouple.readCelsius();
}

float readDrumTemperature() {
  return drumThermocouple.readCelsius();
}
```

#### For Analog Sensors:

Update the conversion formulas based on your sensor's datasheet. See comments in the code.

### 3. Upload Firmware to Arduino

1. Connect Arduino to your computer via USB
2. Open Arduino IDE
3. Open `temp_monitor/temp_monitor.ino`
4. Select **Tools** → **Board** → **Arduino UNO**
5. Select **Tools** → **Port** → (your Arduino's COM port)
6. Click **Upload** button (→)
7. Wait for "Done uploading" message

### 4. Test the Firmware

1. Open **Tools** → **Serial Monitor**
2. Set baud rate to **115200**
3. You should see output like:
   ```
   # Milk Depot Coffee Roaster - Temperature Monitor
   # Ready to send temperature data
   # Format: BT:xxx.x,DT:xxx.x
   BT:23.5,DT:24.1
   BT:23.6,DT:24.1
   BT:23.5,DT:24.2
   ```

## Serial Communication Protocol

### Data Format

Temperature data is sent as comma-separated values:
```
BT:xxx.x,DT:xxx.x\n
```

- **BT**: Bean Temperature in Celsius (1 decimal place)
- **DT**: Drum Temperature in Celsius (1 decimal place)
- Data sent every 1000ms (1 Hz)
- Each line terminated with newline (`\n`)

### Example Output
```
BT:205.3,DT:187.2
BT:206.1,DT:188.5
BT:207.5,DT:190.3
```

### Serial Settings
- **Baud Rate**: 115200
- **Data Bits**: 8
- **Parity**: None
- **Stop Bits**: 1

## Calibration

Temperature probes need calibration for accurate readings.

### Calibration Procedure

1. **Ice Water Test (0°C)**:
   - Fill a container with ice water
   - Stir well and wait for temperature to stabilize
   - Insert both probes and record readings
   - Expected: 0°C ± 1°C

2. **Boiling Water Test (100°C)**:
   - Boil water (at sea level)
   - Insert both probes (be careful!)
   - Record readings
   - Expected: 100°C ± 2°C

3. **Calculate Calibration Values**:
   ```
   offset = 0 - reading_at_0C
   scale = (100 - 0) / (reading_at_100C - reading_at_0C)
   ```

4. **Update Code**:
   Edit these constants in `temp_monitor.ino`:
   ```cpp
   const float BEAN_TEMP_OFFSET = 0.0;   // Your calculated offset
   const float BEAN_TEMP_SCALE = 1.0;    // Your calculated scale
   const float DRUM_TEMP_OFFSET = 0.0;
   const float DRUM_TEMP_SCALE = 1.0;
   ```

5. **Upload and Re-test**: Upload the updated firmware and verify accuracy

### Example Calibration Calculation

If your bean probe reads:
- 2.5°C in ice water (should be 0°C)
- 98.0°C in boiling water (should be 100°C)

```
offset = 0 - 2.5 = -2.5
scale = (100 - 0) / (98.0 - 2.5) = 100 / 95.5 = 1.047
```

Update the code:
```cpp
const float BEAN_TEMP_OFFSET = -2.5;
const float BEAN_TEMP_SCALE = 1.047;
```

## Configuration Options

Edit these constants in `temp_monitor.ino` to customize behavior:

| Constant | Default | Description |
|----------|---------|-------------|
| `BAUD_RATE` | 115200 | Serial communication speed |
| `SAMPLE_INTERVAL_MS` | 1000 | Time between readings (milliseconds) |
| `BEAN_TEMP_PIN` | A0 | Analog pin for bean temp (if using analog) |
| `DRUM_TEMP_PIN` | A1 | Analog pin for drum temp (if using analog) |
| `BEAN_TEMP_OFFSET` | 0.0 | Calibration offset for bean probe |
| `BEAN_TEMP_SCALE` | 1.0 | Calibration scale for bean probe |
| `DRUM_TEMP_OFFSET` | 0.0 | Calibration offset for drum probe |
| `DRUM_TEMP_SCALE` | 1.0 | Calibration scale for drum probe |

## Troubleshooting

### No Data in Serial Monitor

- Check baud rate is set to 115200
- Verify Arduino is powered (LED should be on)
- Check USB cable connection
- Try uploading firmware again

### Temperature Readings are Wrong

- Verify probe connections (check for loose wires)
- Check thermocouple polarity (+ and -)
- Perform calibration procedure
- Test probes individually
- Check for electromagnetic interference

### "NaN" or "-127" Readings

Common with MAX31855/MAX6675 modules:
- Check thermocouple connections
- Verify correct CS (Chip Select) pins
- Check if thermocouple is actually connected to module
- Verify module is powered (VCC and GND)

### Readings are Noisy or Jumping

- Add capacitor across sensor pins (0.1µF)
- Keep wires away from high voltage/current lines
- Use shielded cable for thermocouples
- Increase `SAMPLE_INTERVAL_MS` and average multiple readings

## Development

### Modifying the Firmware

1. Make changes to `temp_monitor.ino`
2. Test thoroughly with Serial Monitor
3. Verify data format is correct
4. Test with actual roasting temperatures
5. Commit changes to git

### Adding Features

Ideas for enhancements:
- Moving average filter for smoother readings
- Error detection and reporting
- Multiple baud rate support
- Temperature alarms/warnings
- Rate of rise (RoR) calculation
- Support for additional sensors (ambient temp, humidity)

## Safety Notes

- K-type thermocouples can measure very high temperatures (up to 1350°C)
- Ensure probes are rated for coffee roasting temperatures (typically 200-250°C)
- Keep electronics away from heat sources
- Use heat-resistant wiring for probes
- Double-check connections before powering on
- Never touch thermocouples during roasting

## Resources

- [MAX31855 Datasheet](https://datasheets.maximintegrated.com/en/ds/MAX31855.pdf)
- [Adafruit MAX31855 Library](https://github.com/adafruit/Adafruit_MAX31855)
- [Arduino Serial Reference](https://www.arduino.cc/reference/en/language/functions/communication/serial/)
- [K-type Thermocouple Guide](https://learn.adafruit.com/thermocouples)

## Version History

- **v1.0** (2025-11-10): Initial release
  - Basic two-probe temperature monitoring
  - Serial communication at 115200 baud
  - Calibration support

## License

MIT License - See main repository for details

## Support

For issues or questions, open an issue on GitHub:
https://github.com/jasonvanwyk/Milk-Depot-Coffee-Roaster/issues
