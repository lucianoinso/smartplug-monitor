# SmartPlug Monitor

A Python tool to read, log, and visualize metrics, usage, and power consumption from a ["Tuya"](https://www.tuya.com/) smart plug.

Supports real-time data collection (voltage, current and power) and visualization of usage patterns through time.
Saves daily logs as CSV files.

## Installation

Clone the repository and install the requirements file.

> Making a virtual environment is strongly suggested

```bash
pip install -r requirements.txt
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

## TODO
- Refactorize the visualization script
- FIX: The logs skip seconds from time to time because it uses `sleep(1)` between calls to not overload the smart plug + the amount of time that the plug takes to answer the request, right now these missing rows can be filled up by using Pandas resample by second `df = df.resample("1s").ffill()`, basically if a row is missing it makes a copy of the last entry before that one, in this case it's totally fine because the values stay constant between seconds.
