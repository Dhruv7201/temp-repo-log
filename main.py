import RPi.GPIO as GPIO
import time
import json
import models
import evdev
import requests
from evdev import InputDevice
import xmltodict

# logging to generate log files
import logging
from datetime import datetime

logging.basicConfig(
    filename=f'/var/prod/log/{datetime.now().strftime("%Y-%m-%d")}_log.txt',
    level=logging.DEBUG,
    format="%(asctime)s - %(message)s",
)
from models import api_models

GPIO.setwarnings(False)
global ready
ready = True
product_get_url = "https://registrationandtouristcare.uk.gov.in:9017/verification/scan/verifyuserbydevice"

GPIO.setmode(GPIO.BCM)
Red = 17
Blue = 27
Green = 22
Buzzer = 23
exp_sts = True

GPIO.setup(Red, GPIO.OUT)
GPIO.setup(Blue, GPIO.OUT)
GPIO.setup(Green, GPIO.OUT)
GPIO.setup(Buzzer, GPIO.OUT)


dev = InputDevice("/dev/input/event0")
print(dev)

scan_codes = {
    # Scancode: ASCIICode
    0: None,
    1: "ESC",
    2: "1",
    3: "2",
    4: "3",
    5: "4",
    6: "5",
    7: "6",
    8: "7",
    9: "8",
    10: "9",
    11: "0",
    12: "-",
    13: "=",
    14: "BKSP",
    15: "TAB",
    16: "Q",
    17: "W",
    18: "E",
    19: "R",
    20: "T",
    21: "Y",
    22: "U",
    23: "I",
    24: "O",
    25: "P",
    26: "[",
    27: "]",
    28: "CRLF",
    29: "LCTRL",
    30: "A",
    31: "S",
    32: "D",
    33: "F",
    34: "G",
    35: "H",
    36: "J",
    37: "K",
    38: "L",
    39: ";",
    40: '"',
    41: "`",
    42: "LSHFT",
    43: "\\",
    44: "Z",
    45: "X",
    46: "C",
    47: "V",
    48: "B",
    49: "N",
    50: "M",
    51: ",",
    52: ".",
    53: "/",
    54: "RSHFT",
    56: "LALT",
    100: "RALT",
}
barcode = []


def process_barcode(bar_code):
    global ready
    payload = {"UniqueCode": bar_code, "VerificationPointId": "2", "MachineCode": "102"}
    logging.info(f"payload for product_post_url_Token = {payload}")
    try:
        r = requests.get(product_get_url, params=payload)
    #         print(r.url)
    except requests.exceptions.RequestException as e:
        print("Network error occurred")
        logging.info(f"Network error occurred")
        for x in range(5):
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(Red, GPIO.OUT)
            GPIO.output(Red, GPIO.HIGH)
            GPIO.setup(Buzzer, GPIO.OUT)
            GPIO.output(Buzzer, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(Red, GPIO.LOW)
            GPIO.output(Buzzer, GPIO.LOW)
            time.sleep(0.2)
        GPIO.cleanup()

        ready = True
        return
    data_dict = [r.json()]
    logging.info(f"responce from product_get_url = {data_dict}")
    print(r.text)
    for item in data_dict:
        responce = str(item.get("status"))
        #         print(responce)

        if str(responce) == str(True):
            GPIO.setmode(GPIO.BCM)
            GPIO.output(Red, GPIO.LOW)
            GPIO.setup(Green, GPIO.OUT)
            GPIO.output(Green, GPIO.HIGH)
            GPIO.output(Red, GPIO.LOW)
            GPIO.setup(Buzzer, GPIO.OUT)
            GPIO.output(Buzzer, GPIO.HIGH)
            GPIO.output(Red, GPIO.LOW)
            time.sleep(0.5)
            GPIO.output(Green, GPIO.LOW)
            GPIO.output(Buzzer, GPIO.LOW)

        else:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(Red, GPIO.OUT)
            GPIO.output(Red, GPIO.HIGH)
            GPIO.setup(Buzzer, GPIO.OUT)
            GPIO.output(Buzzer, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(Red, GPIO.LOW)
            GPIO.output(Buzzer, GPIO.LOW)


for event in dev.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        data = evdev.categorize(event)  # Save the event temporarily to introspect it
        if data.keystate == 1:  # Down events only
            key_lookup = scan_codes.get(data.scancode) or "UNKNOWN:{}".format(
                data.scancode
            )
            if key_lookup == "CRLF":
                barcode_str = "".join(barcode)
                barcode.clear()
                #                 print(f"ready {ready}")

                if ready:
                    if len(barcode_str) > 9:
                        #                         ready = False
                        #                         print(barcode_str)
                        logging.info(f"barcode = {barcode_str}")

                        process_barcode(barcode_str)

            else:
                barcode.append(key_lookup)
