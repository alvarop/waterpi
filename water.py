import os
import time
import yaml
from datetime import datetime, timedelta
import argparse

try:
    import RPi.GPIO as gpio
except Exception as e:
    on_pi = False
else:
    on_pi = True

config = None

parser = argparse.ArgumentParser()

parser.add_argument("config", help="Config file location")

parser.add_argument(
    "--sleep", type=float, default=1.0, help="Scheduling sleep/resolution"
)

args = parser.parse_args()

if not os.path.exists(args.config):
    raise Exception("Config file not found.")


def load_config():
    global config
    with open(args.config, "r") as config_file:
        config = yaml.safe_load(config_file)

    if config is None:
        raise Exception("Unable to load config file")


print("Loading initial configuration")
load_config()

pumps = []

if on_pi:
    gpio.setmode(gpio.BCM)
    print("Enumerating pumps")
    for pump in config["pumps"]:
        print(pump)
        gpio.setup(pump, gpio.OUT, initial=1)
        pumps.append(False)


while True:
    load_config()

    old_pump_values = pumps

    # Assume all pumps are off unless determined otherwise
    pumps = [False] * len(pumps)

    for item in config["schedule"]:
        pump_no = item["pump_no"]
        if item["start_time"] < datetime.now() < item["stop_time"]:
            pumps[pump_no] = True

    for pump_no, enabled in enumerate(pumps):
        if old_pump_values[pump_no] is False and enabled is True:
            print(
                datetime.now(),
                "Starting Pump {}".format(pump_no),
                config["pumps"][pump_no],
            )
            if on_pi:
                gpio.output(config["pumps"][pump_no], 0)
        elif old_pump_values[pump_no] is True and enabled is False:
            print(
                datetime.now(),
                "Stopping Pump {}".format(pump_no),
                config["pumps"][pump_no],
            )
            if on_pi:
                gpio.output(config["pumps"][pump_no], 1)

    time.sleep(args.sleep)
