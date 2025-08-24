from time import sleep
from datetime import datetime
import os
import csv

import tinytuya

CURRENT = "18"
POWER = "19"
VOLTAGE = "20"

LOGS_DIR = "logs"


def get_values(device):
    current_status = device.status()['dps']
    voltage = current_status[VOLTAGE] / 10 # V
    current = current_status[CURRENT] # in mA
    power = current_status[POWER] / 10 # in W
    values = {
        "voltage": voltage,
        "current": current,
        "power": power
    }
    return values


def capture_and_dump(device):
    directory = LOGS_DIR
    if not os.path.exists(directory):
        os.makedirs(directory)

    headers = ["timestamp", "voltage", "current", "power"]

    while True:
        try:
            while True:
                filename = datetime.today().strftime("%Y-%m-%d")    
                csv_path=f"{directory}/{filename}.csv"
                current_status = get_values(device)
                voltage = current_status["voltage"]
                current = current_status["current"]
                power = current_status["power"]
                
                timestamp = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

                row = [timestamp, voltage, current, power]
                file_exists = os.path.isfile(csv_path)

                with open(csv_path, mode="a", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=headers)

                    if not file_exists:
                        writer.writeheader()
                    
                    writer.writerow({
                        "timestamp": timestamp,
                        "voltage": voltage,
                        "current": current,
                        "power": power,
                    })
                    print(f"[{timestamp}] - {current_status}")
                sleep(1)

        except Exception as e:
            print(f"Error: {e}. Restarting loop...")
            sleep(1)


def main():
    device = tinytuya.OutletDevice(
        dev_id = 'YOUR_DEVICE_ID',
        address='Auto',  # Auto-discover IP address
        local_key='YOUR_LOCAL_KEY',
        version=3.4
    )

    try:
        capture_and_dump(device)
    except KeyboardInterrupt:
        print("\nExiting...")


if __name__ == '__main__':
    main()
