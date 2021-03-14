'''
# Use below command to scan for a specified number of lights. Reduces scanning time.
lifx = LifxLAN(num_lights)

# To find a light based on IP and Mac address. Note the router does update the IP address every now and then.
office_light = Light("d0:73:d5:30:6b:a7", "10.0.0.39")
'''
import RPi.GPIO as GPIO
import time
import requests

pir = 23 #input GPIO pin for PIR sensor
last_motion = 0
TURNOFF_DELAY = 60*10

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pir, GPIO.IN)         #Read output from PIR motion sensor

def printTime():
    currentTime = "[" + time.strftime('%a %-d %b %y %H:%M:%S') + "]"
    return currentTime


def init_lights():
    occupied = 0
    last_motion = 0
    # blink lights to show script has initialised
    toggle_lights("off")
    time.sleep(2)
    toggle_lights("on")
    time.sleep(2)
    toggle_lights("off")
    print(printTime(),"--------autolights initiated--------")
    return (occupied, last_motion)


def main():
    occupied, last_motion = init_lights()
    while True:
        i=GPIO.input(pir)
        if i == 1 and occupied == 0:
            last_motion = time.time()
            occupied = 1
            print(printTime(),"turning on lights")
            try:
                toggle_lights("on")
            except:
                print(printTime(),"something went wrong with connecting the lights")
        
        if i == 1 and occupied == 1:
            occupied = 1
            last_motion = time.time()
            time.sleep(1)
        
        if occupied == 1 and time.time() - last_motion >= (TURNOFF_DELAY):
            occupied = 0
            print(printTime(),"no motion for a while turning lights off")
            time.sleep(1)
            try:
                toggle_lights("off")
            except:
                print(printTime(),"something went wrong with connecting to the lights")
        
        time.sleep(1)

def toggle_lights(power="off"):
    url = "https://api.lifx.com/v1/lights/all/toggle"
    headers = {'Authorization': 'Bearer c855bd842b6aef321f4b49ec7c44b7ac86b8c47cf8fb4d6b678160a452402096'} 
    payload = {"power": power}
    response = requests.post(url, headers=headers, data=payload)


if __name__== "__main__":
    main()
