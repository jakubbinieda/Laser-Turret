import requests
import urllib.request
from bs4 import BeautifulSoup
import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)

servoHor = GPIO.PWM(17, 50)
servoVer = GPIO.PWM(27, 50)
servoHor.start(0)
servoVer.start(0)

while 1:
    url = "http://192.168.0.118:8080"
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    print("Ver:"+soup.find("div", {"id": "angleVer"}).get_text()+" Hor:"+soup.find("div", {"id": "angleHor"}).get_text())
    servoHor.ChangeDutyCycle(8-float(soup.find("div", {"id": "angleHor"}).get_text()))
    servoVer.ChangeDutyCycle(float(soup.find("div", {"id": "angleVer"}).get_text()))
    time.sleep(1)