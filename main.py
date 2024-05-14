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

logging.basicConfig(filename=f'/var/prod/log/MCode_102VPoint_2{datetime.now().strftime("%Y-%m-%d")}_log.txt', level=logging.DEBUG, format='%(asctime)s - %(message)s')
from models import api_models
GPIO.setwarnings(False)
global ready
ready = True
product_get_url = 'https://registrationandtouristcare.uk.gov.in:9017/verification/scan/verifyuserbydevice'

GPIO.setmode(GPIO.BCM)
Red = 17
Blue = 27
Green = 22
Buzzer = 23
exp_sts=True

GPIO.setup(Red, GPIO.OUT)
GPIO.setup(Blue, GPIO.OUT)
GPIO.setup(Green, GPIO.OUT)
GPIO.setup(Buzzer, GPIO.OUT)



dev = InputDevice('/dev/input/event0')
print(dev)

scan_codes = {
    # Scancode: ASCIICode
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
}
barcode = []


def process_barcode(bar_code):
    global ready
    payload = {'UniqueCode': bar_code, 'VerificationPointId': '2', 'MachineCode': '102'}
    logging.info(f'payload for product_post_url_Token = {payload}')
    try:
        r = requests.get(product_get_url, params=payload)
#         print(r.url)
    except requests.exceptions.RequestException as e:
        print("Network error occurred")
        logging.info(f'Network error occurred')
        for x in range (5):
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
    data_dict = [r.json()];
    logging.info(f'responce from product_get_url = {data_dict}')
    print(r.text)
    for item in data_dict:
        responce = str(item.get('status'))
#         print(responce)
        
        if (str(responce) == str(True)):
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
            key_lookup = scan_codes.get(data.scancode) or u'UNKNOWN:{}'.format(data.scancode)
            if key_lookup == "CRLF":
                barcode_str = "".join(barcode)
                barcode.clear()
#                 print(f"ready {ready}")

                if ready:
                    if len(barcode_str) > 9:
#                         ready = False
#                         print(barcode_str)
                        logging.info(f'barcode = {barcode_str}')

                        process_barcode(barcode_str)

            else:
                barcode.append(key_lookup)
        
            
                
                
