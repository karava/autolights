import RPi.GPIO as GPIO
import time
from lifxlan import LifxLAN

pir = 23 #input GPIO pin for PIR sensor
last_motion = 0
num_lights = 2

# lights are: 'Main light' and 'Reading lamp'

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pir, GPIO.IN)         #Read output from PIR motion sensor
# GPIO.setup(3, GPIO.OUT)         #LED output pin


def main():
    occupied = 0
    last_motion = 0
    lifx = LifxLAN(num_lights)
    office_light = lifx.get_device_by_name('Main light')
    reading_lamp = lifx.get_device_by_name('Reading lamp')
    
    # blink lights to show script has initialised
    # in the future make all lights blink
    office_light.set_power(0)
    time.sleep(1)
    office_light.set_power(65535)
    time.sleep(1)
    office_light.set_power(0)

    while True:
        i=GPIO.input(pir)
        try:
            if i == 1 and occupied == 0:
                last_motion = time.time()
                occupied = 1

                print("turning on lights", time.strftime('%a %-d %b %y %H:%M:%S'))
                #print("turning on lights", time.strftime('%-d %a %y %H:%M:%S'))
                office_light.set_power(65535)

            if i == 1 and time.time() - last_motion <= (60*15):
                occupied = 1
                last_motion = time.time()
                #print("keeping lights on")
            elif occupied != 0:
                occupied = 0
                print("no motion for a while turning lights off", time.strftime('%a %H:%M:%S'))
                office_light.set_power("off")
                reading_lamp.set_power("off")
        
        except Exception:
            print("Something went wrong")

        time.sleep(1)


if __name__== "__main__":
    main()
