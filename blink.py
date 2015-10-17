import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

blink_time = 1

try:
    while True:
        GPIO.output(7,True)
        time.sleep(blink_time)
        GPIO.output(7,False)
        time.sleep(blink_time)
        
except KeyboardInterrupt:
    GPIO.cleanup()
