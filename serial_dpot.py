#!/usr/bin/python

## MCP4131 docs: http://dlnmh9ip6v2uc.cloudfront.net/datasheets/Components/General%20IC/22060b.pdf
## some codes: http://electronics.stackexchange.com/questions/94479/digital-potentiometer-mcp4131-with-raspberry-pi

import sys
import time
import signal
import argparse

import RPi.GPIO as GPIO

SPI_CS_PIN = 17
SPI_SDISDO_PIN = 22 # mosi
SPI_CLK_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(SPI_CS_PIN, GPIO.OUT)
GPIO.setup(SPI_CLK_PIN, GPIO.OUT)
GPIO.setup(SPI_SDISDO_PIN, GPIO.OUT)

GPIO.output(SPI_CLK_PIN, False)
GPIO.output(SPI_SDISDO_PIN, False)
GPIO.output(SPI_CS_PIN, False)

GPIO.output(SPI_CS_PIN, True)
GPIO.output(SPI_CLK_PIN, False)
GPIO.output(SPI_CS_PIN, False)


def set_value(value):
    b = '{0:016b}'.format(value)
    for x in range(0, 16):
        GPIO.output(SPI_SDISDO_PIN, int(b[x]))

        GPIO.output(SPI_CLK_PIN, True)
        GPIO.output(SPI_CLK_PIN, False)

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
    ## signal sends us args that we don't care about. We will need to be able to accpet them though, hense *args.
    set_value(255)
    GPIO.cleanup()
    exit(0)

def main(level=62, delay=0.03):
    signal.signal(signal.SIGINT, quit_gracefully)
    try:
        fade(level,delay)
    except KeyboardInterrupt:
        quit_gracefully()

if __name__ == "__main__":
    main()
