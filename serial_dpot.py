#!/usr/bin/python

## MCP4131 docs: http://cdn.sparkfun.com/datasheets/Components/General%20IC/22060b.pdf
## some (liberally borrowed from) codes: http://electronics.stackexchange.com/questions/94479/digital-potentiometer-mcp4131-with-raspberry-pi

import sys
import time
import signal
import argparse

import RPi.GPIO as GPIO

## These numbers will corrispond do the pin numbers printed on my GPIO breadboard breakout. They will depend on the GPIO.setmode you use.
SPI_CS_PIN = 17 ## Chip Select
SPI_SDISDO_PIN = 22 ## Serial Interface
SPI_CLK_PIN = 23 ## Clock

## This picks the way we would like to assigne the mode. BCM is short for Broadcom. The other option is BOARD. 
## This can get fiddly, see: http://raspberrypi.stackexchange.com/questions/12966/what-is-the-difference-between-board-and-bcm-for-gpio-pin-numbering
GPIO.setmode(GPIO.BCM)

## This is binding some pin numbers and variable names and telling the library that we will be outputing to them.
## If we wanted to we could skip the variable names and just use pin numbers all the time, but that would be a pain and very hard to read.
GPIO.setup(SPI_CS_PIN, GPIO.OUT)
GPIO.setup(SPI_CLK_PIN, GPIO.OUT)
GPIO.setup(SPI_SDISDO_PIN, GPIO.OUT)

"""
The Chip Select (CS) signal is used to select the device and frame a command sequence. To start a command,
or sequence of commands, the CS signal must transition from the inactive state (VIH) to an active state
(VIL or VIHH).

After the CS signal has gone active, the SDO pin is driven and the clock bit counter is reset. The Chip Select (CS)
signal is used to select the device and frame a command sequence. To start a command, or sequence of commands, the
CS signal must transition from the inactive state (VIH) to an active state (VIL or VIHH).

After the CS signal has gone active, the SDO pin is driven and the clock bit counter is reset. 
"""
GPIO.output(SPI_CS_PIN, True) ## VIH 3.3 V, inactive
GPIO.output(SPI_CS_PIN, False) ## VIL 0 V, active

def set_value(value):
    b = '{0:016b}'.format(value) ## TODO Try to get this to work with 8 bit.
    for x in range(0,16):
        GPIO.output(SPI_SDISDO_PIN, int(b[x])) # Send input to the serial pin (this is of course binary, hi / low, 3.3V / 0V)

        ## Cycle the clock. Must be cycled for every literal bit of serial input.
        GPIO.output(SPI_CLK_PIN, True)
        GPIO.output(SPI_CLK_PIN, False)
        ## There was evening, and there was morning--the nth day.

def discrete_value_from_input(level):
    while True:
        print 'level:' + str(level)
        set_value(level)
        level = int(raw_input('enter level (1 - 40)\n'))

def fade(level,delay):
        while True:
    #       for level in range(0, 256):
            for level in range(0, 40):
                print 'level:' + str(level)
                set_value(level)
                time.sleep(delay)

    #       for level in range(255, -1, -1):
            for level in range(40, -1 , -1):
                print 'level:' + str(level)
                set_value(level)
                time.sleep(delay)

def quit_gracefully(*args):
    ## Signal sends us args that we don't care about. We will need to be able to accpet them though, hense *args.
    set_value(255) ## Set resistance high to cut of LED
    GPIO.cleanup()
    exit(0)

def main(level=62, delay=0.03):
    signal.signal(signal.SIGINT, quit_gracefully) ## I have this here so I can send this process a keyboard interruppted when it's running in the background.
    try:
        fade(level,delay)
    except KeyboardInterrupt:
        quit_gracefully()

if __name__ == "__main__":
    main()
