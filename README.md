# SmartPlug Monitor

A Python tool to read, log, and visualize metrics, usage, and power consumption from a ["Tuya"](https://www.tuya.com/) smart plug.

Supports real-time data collection (voltage, current and power) and visualization of usage patterns through time.
Saves daily logs as CSV files.

## Installation

1. Clone the repository and install the requirements file.

> Using a virtual environment is strongly suggested

```bash
pip install -r requirements.txt
```

2. Follow the [Tinytuya device preparation guide](https://github.com/jasonacox/tinytuya#tuya-device-preparation) to connect with your device.
3. Replace `YOUR_DEVICE_ID` and `YOUR_LOCAL_KEY` in `main()` inside the `monitor.py` file, with your smart plug credentials.

## Usage

### To start capturing data from your device:

```bash
python monitor.py
```
You can find the generated logs inside the `logs/` directory.

### To visualize the metrics of a specific file

```bash
python visualize_usage.py <filename>
```
> `filename` is the name of the file **inside** the `logs` directory (there's no need to add `logs/` to this argument).


## CSV Structure

Each CSV file contains the following columns:

- `timestamp` – date and time of the measurement
- `voltage` – voltage in volts (V)
- `current` – current in milliamps (mA)
- `power` – power in watts (W)

## Sample output

![Example Plot](plots/plot_sample.png)
