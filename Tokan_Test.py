import RPi.GPIO as GPIO
import time

import logging

logging.basicConfig(filename=f'/var/prod/log/{datetime.now().strftime("%Y-%m-%d")}_log.txt', level=logging.DEBUG, format='%(asctime)s - %(message)s')


import json
import evdev
from datetime import datetime
from escpos.printer import File
import requests
from evdev import InputDevice

GPIO.setwarnings(False)
global ready
ready = True
product_get_url_Verification= 'https://registrationandtouristcare.uk.gov.in:9017/verification/scan/verifyuserbydevice'
product_post_url_Token= 'https://registrationandtouristcare.uk.gov.in:9017/verification/scan/generatemachinetoken'
p = File('/dev/usb/lp0')
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


def get_newline(line):
    result = ''
    for x in range(line):
        result += '\n'
    return result

def process_barcode_Token(bar_code):
    global ready
    payload = {'UniqueCode': bar_code, 'VerificationPointId': '20', 'MachineCode': '171'}
    logging.info(f'payload for product_post_url_Token = {payload}')
    try:
        t = requests.post(product_post_url_Token, params=payload)
        print(t.text)
        result = json.loads(t.text)
        logging.info(f'response from product_post_url_Token = {result}')
        data_dict = [t.json()];
        for item in data_dict:
            responce = str(item.get('status'))
            curDTObj = datetime.now()
            dateStr = curDTObj.strftime("%d %b, %Y")
            p.set(align=u"center",width=1,height=1)
            if (str(responce) == str(True)):
                for x in result['data']['header']:
                  p.set(align= u"" + x['align'],width=x['width'] ,height=x['height'],text_type=x['text_type'])
                  p.text(get_newline(x['newlinefront']) + x['Label'] + get_newline(x['newlineback']))
                 

                p.text("------------------------\n")
                p.qr(barcode_str,size=8)
                p.set(align=u"center",width=1 ,height=1)
                p.text(barcode_str +"\n")
                p.set(align=u"center",width=2 ,height=2)

                for x in result['data']['body']:
                  p.set(align= u"" + x['align'],width=x['width'] ,height=x['height'],text_type=x['text_type'])
                  p.text(get_newline(x['newlinefront']) + x['Label'] + get_newline(x['newlineback']))
                  

                p.text("------------------------------------------------\n")
                p.set(align=u"center",width=1,height=1)
                for x in result['data']['footer']:
                  p.set(align= u"" + x['align'],width=x['width'] ,height=x['height'],text_type=x['text_type'])
                  p.text(get_newline(x['newlinefront']) + x['Label'] + get_newline(x['newlineback']))
                  
                
                p.cut()

            else:
                p.set(align=u"center",width=2,height=2)
                p.text("Uttarakhand Tourism \n")
                p.text("------------------------\n\n\n")
                p.text("No Slots Available Now  \n\n\n")
                p.set(align=u"center",width=1 ,height=1)
                curDTObj = datetime.now()
                dateStr = curDTObj.strftime("%d %b, %Y")
                p.text("Date : " + dateStr +" \n")
                p.text("------------------------------------------------\n")
                p.set(align=u"center",width=1,height=1)
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
        logging.info(f'Network error occurred')
    print(t.text)

def process_barcode_Verification(bar_code):
    global ready
    payload = {'UniqueCode': bar_code, 'VerificationPointId': '20', 'MachineCode': '171'}
    logging.info(f'payload to product_get_url_Verification {payload}')
    try:
        r = requests.get(product_get_url_Verification, params=payload)
        
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
    logging.info(f'response from product_get_url_Verification = {data_dict}')
    print(r.text)
    
    for item in data_dict:
        responce = str(item.get('status'))
#         print(responce)
        
        if (str(responce) == str(True)):
            
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
            key_lookup = scan_codes.get(data.scancode) or u'UNKNOWN:{}'.format(data.scancode)
            if key_lookup == "CRLF":
                barcode_str = "".join(barcode)
                barcode.clear()

                if ready:
                    if len(barcode_str) > 9:
#                       print(barcode_str)
                        logging.info(f'barcode = {barcode_str}')
                        process_barcode_Verification(barcode_str)
                        

            else:
                barcode.append(key_lookup)
                
