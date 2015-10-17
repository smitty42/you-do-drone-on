import time

import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.IN)

blink_time = .1

toggle = False

try:
    while True:
        butt_state = not bool(GPIO.input(11))
        if butt_state and not toggle:
            toggle = True
            butt_state = False
            time.sleep(.2)
            
        if toggle and butt_state:
            toggle = False
            butt_state = False
            time.sleep(.2)

        if toggle:
            GPIO.output(7,True)
        else:
            GPIO.output(7,False)
        
except KeyboardInterrupt:
    GPIO.cleanup()
