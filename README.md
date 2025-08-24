Read, log, and visualize data from "Tuya" smart plugs. Supports real-time data collection and visualization of usage patterns through time.

# SmartPlug Monitor

A Python tool to read, log, and analyze power consumption from a "Tuya" smart plug.
Supports real-time data collection (voltage, current and power) and visualization of usage patterns through time.
Saves daily logs as CSV files.

## Installation

```bash
git clone https://github.com/yourusername/smartplug-monitor.git
cd smartplug-monitor
pip install tinytuya
```

## Usage

0. Follow the [Tinytuya guide](https://github.com/jasonacox/tinytuya) to prepare and connect with your device.
1. Replace `YOUR_DEVICE_ID` and `YOUR_LOCAL_KEY` in `main()` with your smart plug credentials.
2. Run the script:

```bash
python monitor.py
```

3. Check the `logs/` directory for the daily generated logs CSV files.

## CSV Structure

Each CSV file contains the following columns:

- `timestamp` – date and time of the measurement
- `voltage` – voltage in volts (V)
- `current` – current in milliamps (mA)
- `power` – power in watts (W)

