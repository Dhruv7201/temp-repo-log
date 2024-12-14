import RPi.GPIO as GPIO
GPIO.setwarnings(False)
import time

GPIO.setmode(GPIO.BCM)
Red = 17
Blue = 27
Green = 22
Buzzer = 23

GPIO.setup(Red, GPIO.OUT)
GPIO.setup(Blue, GPIO.OUT)
GPIO.setup(Green, GPIO.OUT)
GPIO.setup(Buzzer, GPIO.OUT)

GPIO.output(Red, GPIO.HIGH)
GPIO.output(Blue, GPIO.HIGH)
GPIO.output(Green, GPIO.HIGH)
GPIO.output(Buzzer, GPIO.HIGH)

time.sleep(13)

GPIO.output(Red, GPIO.LOW)
GPIO.output(Blue, GPIO.LOW)
GPIO.output(Green, GPIO.LOW)
GPIO.output(Buzzer, GPIO.LOW)

GPIO.cleanup()






