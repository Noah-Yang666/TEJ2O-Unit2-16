"""
Created by: Noah Yang
Created on: April 2026
This module is a Micro:bit MicroPython program that uses radio to transmit and receive messages
"""

from microbit import *

import radio


class HCSR04:
    # this class abstracts out the functionality of the HC-SR04 and
    #   returns distance in mm
    # Trig: pin 1
    # Echo: pin 2
    def __init__(self, tpin=pin1, epin=pin2, spin=pin13):
        self.trigger_pin = tpin
        self.echo_pin = epin
        self.sclk_pin = spin

    def distance_mm(self):
        spi.init(
            baudrate=125000,
            sclk=self.sclk_pin,
            mosi=self.trigger_pin,
            miso=self.echo_pin,
        )
        pre = 0
        post = 0
        k = -1
        length = 200
        resp = bytearray(length)
        resp[0] = 0xFF
        spi.write_readinto(resp, resp)
        # find first non zero value
        try:
            i, value = next((ind, v) for ind, v in enumerate(resp) if v)
        except StopIteration:
            i = -1
        if i > 0:
            pre = bin(value).count("1")
            # find first non full high value afterwards
            try:
                k, value = next(
                    (ind, v)
                    for ind, v in enumerate(resp[i : length - 2])
                    if resp[i + ind + 1] == 0
                )
                post = bin(value).count("1") if k else 0
                k = k + i
            except StopIteration:
                i = -1
        dist = -1 if i < 0 else round(((pre + (k - i) * 8.0 + post) * 8 * 0.344) / 2)
        return dist


# variables needed
sonar = HCSR04()
numberDistance = 0

# setting up
display.clear()
display.show(Image.HAPPY)
radio.config(group=67)
radio.on()

# start tracking with button A
while True:
    if button_a.was_pressed():
        while True:
            display.show(str(numberDistance) + "cm")
            if sonar.distance_mm() / 10 < 5:
                display.show(Image.TRIANGLE)
                radio.send("Too Close")
            else:
                display.show(Image.TRIANGLE)
                radio.send("It's Good")
    message = radio.receive()
    if message:
        display.clear()
        display.scroll(message)
        display.show(Image.HAPPY)
