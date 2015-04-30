#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as gpio


class light(object):
    def __init__(self,pin_switch_out=0,pin_light1=0):
        self.pin_switch_out=pin_switch_out
	self.pin_light1=pin_light1

        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)

        
        if self.pin_switch_out > 0:
            gpio.setup(self.pin_switch_out, gpio.IN, pull_up_down=gpio.PUD_UP)
        if self.pin_light1 > 0:
            gpio.setup(self.pin_light1, gpio.OUT)
            gpio.output(self.pin_light1, False)   
    
    
    def finish(self):
        gpio.cleanup()
