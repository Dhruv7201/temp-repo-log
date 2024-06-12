import json
import models
import evdev
import requests
from evdev import InputDevice
import xmltodict
#from vend_logic import spiral_vend
from models import api_models

#377740668482
377740668482
machine_id = "123"
global ready
ready = True
product_get_url = 'http://115.124.96.40:8095/verification/scan/verifyuserbydevice'


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
    payload = {'UniqueCode': bar_code, 'VerificationPointId': '111'}
    try:
        r = requests.get(product_get_url, params=payload)
        print(r.url)
    except requests.exceptions.RequestException as e:
        print("Network error occurred")
        ready = True
        return
    data_dict = [];
    
    
    print(r.text)
    for item in data_dict:
        tray = int(item.get('Item_Tray_No'))
        partition = int(item.get('Item_Tray_Slot'))
        vend_qty = item.get('Item_Qty')

        for i in range(0, vend_qty):
            print(f"Tray :{tray} , Partition : {partition} ")
            sv = SpiralVend(tray, partition)
            try:
                vend_data = spiral_vend.MultiVend(sv).vend()
                print(vend_data.get('vend'))
                if vend_data.get('vend'):
                    vending_status = "Success"
                else:
                    vending_status = "Failed"
                vend_response = api_models.VendResponse(machine_id, item.get("SR_No"), vending_status,
                                                        item.get("OPDD_ID"))
                if i+1 == vend_qty:
                    vend_response_array.append(vend_response)
            except Exception as e:
                ready = True

for event in dev.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        data = evdev.categorize(event)  # Save the event temporarily to introspect it
        if data.keystate == 1:  # Down events only
            key_lookup = scan_codes.get(data.scancode) or u'UNKNOWN:{}'.format(data.scancode)
            if key_lookup == "CRLF":
                barcode_str = "".join(barcode)
                barcode.clear()
                print(f"ready {ready}")

                if ready:
                    if len(barcode_str) > 5:
#                         ready = False
                        print(barcode_str)
                        process_barcode(barcode_str)

            else:
                barcode.append(key_lookup)
                
                


