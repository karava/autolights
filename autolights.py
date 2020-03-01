import RPi.GPIO as GPIO
import time
from lifxlan import LifxLAN, Light

pir = 23 #input GPIO pin for PIR sensor
last_motion = 0
num_lights = 2
TURNOFF_DELAY = 60*10

# lights are: 'Main light' and 'Reading lamp'

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pir, GPIO.IN)         #Read output from PIR motion sensor
# GPIO.setup(3, GPIO.OUT)         #LED output pin


def main():
    occupied = 0
    last_motion = 0
    lifx = LifxLAN(num_lights)
    office_light = Light("d0:73:d5:30:6b:a7", "10.0.0.39")
    #office_light = lifx.get_device_by_name('Main light')
    print(office_light.get_mac_addr())
    print(office_light.get_ip_addr())
    # reading_lamp = lifx.get_device_by_name('Reading lamp')
    
    # blink lights to show script has initialised
    # in the future make all lights blink
    office_light.set_power(0)
    time.sleep(1)
    office_light.set_power(65535)
    time.sleep(1)
    office_light.set_power(0)
    print("autolights initiated", time.strftime('%c'))

    while True:
        i=GPIO.input(pir)
        if i == 1 and occupied == 0:
            last_motion = time.time()
            occupied = 1

            print("turning on lights", time.strftime('%a %-d %b %y %H:%M:%S'))
            #print("turning on lights", time.strftime('%-d %a %y %H:%M:%S'))
            try:
                office_light.set_power(65535)
            except:
                print("something went wrong with connecting the lights")
        
        if i == 1 and occupied == 1:
            occupied = 1
            last_motion = time.time()
            try:
                if office_light.get_power() < 1:
                    office_light.set_power(65535)
                    print("recovered lights")
            except:
                print("failed to recover lights")
        
        if occupied == 1 and time.time() - last_motion >= (TURNOFF_DELAY):
            occupied = 0
            print("no motion for a while turning lights off", time.strftime('%a %H:%M:%S'))
            try:
                office_light.set_power("off")
                # reading_lamp.set_power("off")
            except:
                print("something went wrong with connecting to the lights")

        time.sleep(1)


if __name__== "__main__":
    main()
