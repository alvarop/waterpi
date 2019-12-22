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


load_config()

if on_pi:
    gpio.setmode(gpio.BCM)
    for pump in config["pumps"]:
        gpio.setup(pump, gpio.OUT, initial=1)

while True:
    load_config()

    for item in config["schedule"]:
        if item["start_time"] < datetime.now() < item["stop_time"]:
            print(
                datetime.now(),
                "Running Pump {}".format(item["pump_no"]),
                config["pumps"][item["pump_no"]],
            )

    time.sleep(args.sleep)
