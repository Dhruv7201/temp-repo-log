import RPi.GPIO as GPIO
import time

from datetime import datetime
import logging

logging.basicConfig(
    filename=f'/var/prod/log/{datetime.now().strftime("%Y-%m-%d")}_log.txt',
    level=logging.DEBUG,
    format="%(asctime)s - %(message)s",
)

import json
import evdev
from datetime import datetime
from escpos.printer import File
import requests
from evdev import InputDevice

GPIO.setwarnings(False)
global ready
ready = True
product_get_url_Verification = "https://registrationandtouristcare.uk.gov.in:9017/verification/scan/verifyuserbydevice"
product_post_url_Token = "https://registrationandtouristcare.uk.gov.in:9017/verification/scan/generatemachinetoken"
p = File("/dev/usb/lp0")
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


def get_newline(line):
    result = ""
    for x in range(line):
        result += "\n"
    return result


def process_barcode_Token(bar_code):
    global ready
    payload = {
        "UniqueCode": bar_code,
        "VerificationPointId": "32",
        "MachineCode": "171",
    }
    logging.info(f"payload for product_post_url_Token = {payload}")

    try:
        t = requests.post(product_post_url_Token, params=payload)
        print(t.text)
        result = json.loads(t.text)
        logging.info(f"response from product_post_url_Token = {result}")
        data_dict = [t.json()]
        for item in data_dict:
            responce = str(item.get("status"))
            curDTObj = datetime.now()
            dateStr = curDTObj.strftime("%d %b, %Y")
            p.set(align="center", width=1, height=1)
            if str(responce) == str(True):
                for x in result["data"]["header"]:
                    p.set(
                        align="" + x["align"],
                        width=x["width"],
                        height=x["height"],
                        text_type=x["text_type"],
                    )
                    p.text(
                        get_newline(x["newlinefront"])
                        + x["Label"]
                        + get_newline(x["newlineback"])
                    )

                response_barcode = item["data"].get("uniqueCode")

                p.text("------------------------\n")
                # p.qr(barcode_str,size=8)
                p.qr(response_barcode, size=8)
                p.set(align="center", width=1, height=1)

                # p.text(barcode_str +"\n")
                p.text(response_barcode + "\n")

                p.set(align="center", width=2, height=2)

                for x in result["data"]["body"]:
                    p.set(
                        align="" + x["align"],
                        width=x["width"],
                        height=x["height"],
                        text_type=x["text_type"],
                    )
                    p.text(
                        get_newline(x["newlinefront"])
                        + x["Label"]
                        + get_newline(x["newlineback"])
                    )

                p.text("------------------------------------------------\n")
                p.set(align="center", width=1, height=1)
                for x in result["data"]["footer"]:
                    p.set(
                        align="" + x["align"],
                        width=x["width"],
                        height=x["height"],
                        text_type=x["text_type"],
                    )
                    p.text(
                        get_newline(x["newlinefront"])
                        + x["Label"]
                        + get_newline(x["newlineback"])
                    )

                p.cut()

            else:
                p.set(align="center", width=2, height=2)
                p.text("Uttarakhand Tourism \n")
                p.text("------------------------\n\n\n")
                p.text("No Slots Available Now  \n\n\n")
                p.set(align="center", width=1, height=1)
                curDTObj = datetime.now()
                dateStr = curDTObj.strftime("%d %b, %Y")
                p.text("Date : " + dateStr + " \n")
                p.text("------------------------------------------------\n")
                p.set(align="center", width=1, height=1)
                p.text("Powered by: Ethics Infotech")
                p.cut()

            # if (str(responce) == str(True)):
            #     Token = str(result['data']['tockenNo'])
            #     Location = str (result['data']['destinationName'])
            #     p.set(align=u"center",width=2,height=2)
            #     curDTObj = datetime.now()
            #     dateStr = curDTObj.strftime("%d %b, %Y")
            #     p.text("Darshan Slot Date : " + dateStr +" \n")
            #     p.set(align=u"center",width=1 ,height=1)

            #     p.text("Uttarakhand Tourism \n")
            #     p.text("Location : "+Location +" \n")
            #     p.text("------------------------\n")
            #     p.qr(barcode_str,size=8)
            #     p.set(align=u"center",width=1 ,height=1)
            #     p.text(barcode_str +"\n")
            #     p.set(align=u"center",width=2 ,height=2)
            #     p.text("\nToken No:"+Token +"\n")
            #     p.set(align=u"center",width=1 ,height=1)
            #     p.text("\n"+ str(result['data']['darshanslottime']) +"\n")
            #     p.set(align=u"center",width=1 ,height=1)
            #     p.text("\n"+ str(result['data']['scantime']) +"\n")
            #     p.set(align=u"center",width=1 ,height=1)
            #     p.text("\n"+ str(result['data']['waitingtime']) +"\n")
            #     p.text("------------------------------------------------\n")

            #     p.set(align=u"center",width=1,height=1)
            #     p.text("\nPowered by: Ethics Infotech\n\n")
            #     p.set(align=u"center",width=1,height=1)
            #     p.text("\nPlease Visit Temple in the given Slot Time\n")
            #     p.cut()
            #     print("print ok")

            # else:
            #     p.set(align=u"center",width=2,height=2)
            #     p.text("Uttarakhand Tourism \n")
            #     p.text("------------------------\n\n\n")
            #     p.text("No Slots Available Now  \n\n\n")
            #     p.set(align=u"center",width=1 ,height=1)
            #     curDTObj = datetime.now()
            #     dateStr = curDTObj.strftime("%d %b, %Y")
            #     p.text("Date : " + dateStr +" \n")
            #     p.text("------------------------------------------------\n")
            #     p.set(align=u"center",width=1,height=1)
            #     p.text("Powered by: Ethics Infotech")
            #     p.cut()
            #         print(r.url)
    except requests.exceptions.RequestException as e:
        print("Network error occurred")
        logging.info(f"Network error occurred")
    print(t.text)


def process_barcode_Verification(bar_code):
    global ready
    payload = {
        "UniqueCode": bar_code,
        "VerificationPointId": "32",
        "MachineCode": "171",
    }
    logging.info(f"payload for product_post_url_Token = {payload}")
    try:
        r = requests.get(product_get_url_Verification, params=payload)

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
    logging.info(f"response from product_get_url_Verification = {data_dict}")

    print(r.text)

    for item in data_dict:
        responce = str(item.get("status"))
        #         print(responce)

        if str(responce) == str(True):
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(Green, GPIO.OUT)
            GPIO.output(Green, GPIO.HIGH)
            #             print("Green On")
            GPIO.setup(Buzzer, GPIO.OUT)
            GPIO.output(Buzzer, GPIO.HIGH)
            time.sleep(1)
            if len(barcode_str) > 9:
                #                 print(barcode_str)
                process_barcode_Token(barcode_str)

            print(barcode_str)

            GPIO.output(Green, GPIO.LOW)
            #             print("Green Off")
            GPIO.output(Buzzer, GPIO.LOW)

        else:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(Red, GPIO.OUT)
            GPIO.output(Red, GPIO.HIGH)
            print("Red On")
            GPIO.setup(Buzzer, GPIO.OUT)
            GPIO.output(Buzzer, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(Red, GPIO.LOW)
            print("Red Off")
            GPIO.output(Buzzer, GPIO.LOW)


for event in dev.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        data = evdev.categorize(event)  # Save the event temporarily to introspect it
        if data.keystate == 1:
            key_lookup = scan_codes.get(data.scancode) or "UNKNOWN:{}".format(
                data.scancode
            )
            if key_lookup == "CRLF":
                barcode_str = "".join(barcode)
                barcode.clear()

                if ready:
                    if len(barcode_str) > 9:
                        #                       print(barcode_str)
                        logging.info(f"barcode = {barcode_str}")
                        process_barcode_Verification(barcode_str)

            else:
                barcode.append(key_lookup)
