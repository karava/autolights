import RPi.GPIO as GPIO
import time
from lifxlan import LifxLAN, Light

pir = 23 #input GPIO pin for PIR sensor
last_motion = 0
num_lights = 2
TURNOFF_DELAY = 60*10

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pir, GPIO.IN)         #Read output from PIR motion sensor

def printTime():
    currentTime = "[" + time.strftime('%a %-d %b %y %H:%M:%S') + "]"
    return currentTime

def main():
    occupied = 0
    last_motion = 0
    office_light = Light("d0:73:d5:30:6b:a7", "10.0.0.39")
    # blink lights to show script has initialised
    office_light.set_power(0)
    time.sleep(2)
    office_light.set_power(65535)
    time.sleep(2)
    office_light.set_power(0)
    print(printTime(),"--------autolights initiated--------")
    while True:
        i=GPIO.input(pir)
        if i == 1 and occupied == 0:
            last_motion = time.time()
            occupied = 1
            print(printTime(),"turning on lights")
            try:
                office_light.set_power(65535)
            except:
                print(printTime(),"something went wrong with connecting the lights")
        
        if i == 1 and occupied == 1:
            occupied = 1
            last_motion = time.time()
            time.sleep(1)
            try:
                if office_light.get_power() < 1:
                    time.sleep(1)
                    office_light.set_power(65535)
                    print(printTime(),"recovered lights")
            except:
                print(printTime(),"failed to recover lights")
        
        if occupied == 1 and time.time() - last_motion >= (TURNOFF_DELAY):
            occupied = 0
            print(printTime(),"no motion for a while turning lights off")
            time.sleep(1)
            try:
                office_light.set_power("off")
            except:
                print(printTime(),"something went wrong with connecting to the lights")
        
        time.sleep(1)


if __name__== "__main__":
    main()
