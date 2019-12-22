import os
import time
import yaml
import uuid
from datetime import datetime, timedelta
from flask import Flask, request, g, render_template, jsonify, Response, redirect

try:
    import RPi.GPIO as gpio
except Exception as e:
    on_pi = False
else:
    on_pi = True


def load_config():
    global config
    with open(CONFIG_PATH, "r") as config_file:
        config = yaml.safe_load(config_file)

    if config is None:
        raise Exception("Unable to load config file")

    # Remove expired items
    to_remove = []
    for item in config["schedule"]:
        if item["stop_time"] < datetime.now():
            to_remove.append(item)

    if len(to_remove) > 0:
        for item in to_remove:
            print("Event {} has expired. Removing".format(item["name"]))
            config["schedule"].remove(item)
        save_config()


def save_config():
    global config
    with open(CONFIG_PATH, "w") as outfile:
        yaml.dump(config, outfile, default_flow_style=False)


app = Flask(__name__)

config = None

DEFAULT_CONFIG_PATH = "./config.yml"
CONFIG_PATH = os.getenv("CONFIG")

DEFAULT_CONFIG = {"schedule": [], "pumps": [22, 27, 17, 23]}

if CONFIG_PATH is None:
    print("Config file not specified. Using local config")
    CONFIG_PATH = DEFAULT_CONFIG_PATH

if not os.path.exists(CONFIG_PATH):
    print("Config file not found. Creating...")
    with open(CONFIG_PATH, "w") as outfile:
        yaml.dump(DEFAULT_CONFIG, outfile, default_flow_style=False)

load_config()

if on_pi:
    gpio.setmode(gpio.BCM)
    for pump in config["pumps"]:
        gpio.setup(pump, gpio.OUT, initial=1)


def pumpctl(pump_no, state):
    if not on_pi:
        return False

    if pump_no >= len(config["pumps"]) or pump_no < 0:
        return False

    gpio.output(config["pumps"][pump_no], state)

    return True


@app.route("/debug")
def list():
    return render_template("debug.html", pumps=config["pumps"])


@app.route("/enable/<pump_no>")
def enable(pump_no):
    print("Enabling pump {}".format(int(pump_no)))
    pumpctl(int(pump_no), 0)
    return "OK"


@app.route("/disable/<pump_no>")
def disable(pump_no):
    print("Disabling pump {}".format(int(pump_no)))
    pumpctl(int(pump_no), 1)
    return "OK"


@app.route("/")
def main():
    return redirect("/schedule")


@app.route("/schedule")
def schedule():
    load_config()
    return render_template("schedule.html", config=config)


@app.route("/add", methods=["POST"])
def add():
    load_config()

    start_str = "{} {}".format(request.form["start_date"], request.form["start_time"])

    stop_str = "{} {}".format(request.form["stop_date"], request.form["stop_time"])

    start_time = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
    stop_time = datetime.strptime(stop_str, "%Y-%m-%d %H:%M")

    pump_no = int(request.form["pump_no"])

    if start_time >= stop_time:
        return "Error. Start time is after stop time!"

    if pump_no >= len(config["pumps"]) or pump_no < 0:
        return "Error. Invalid pump!"

    config["schedule"].append(
        {
            "name": request.form["name"],
            "start_time": start_time,
            "stop_time": stop_time,
            "pump_no": pump_no,
            "uuid": str(uuid.uuid4()),
        }
    )

    config["schedule"] = sorted(config["schedule"], key=lambda x: x["start_time"])

    save_config()

    return redirect("/schedule")


@app.route("/delete", methods=["POST"])
def delete():
    load_config()

    for item in config["schedule"]:
        if item["uuid"] == request.form["uuid"]:
            config["schedule"].remove(item)

    save_config()

    return redirect("/schedule")
