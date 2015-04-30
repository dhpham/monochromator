#!/usr/bin/python
# -*- coding: utf-8 -*-

# Simple example of the easydriver Python library.
# Dave Finch 2013

import easydriver as ed
import time

# Direction of rotation is dependent on how the motor is connected.
# If the motor runs the wrong way swap the values of cw and ccw.
cw = True
ccw = False


'''Arguments to pass or set up after creating the instance.

Step GPIO pin number.
Delay between step pulses in seconds.
Direction GPIO pin number.
Microstep 1 GPIO pin number.
Microstep 2 GPIO pin number.
#Microstep 3 GPIO pin number.
Sleep GPIO pin number.
Enable GPIO pin number.
Reset GPIO pin number.
Name as a string.'''


# Create an instance of the easydriver class.
# Not using sleep, enable or reset in this example.
stepper = ed.easydriver(24, 0.05, 23, 20, 21, 25, 22)

#stepper.change_delay(0.1)
# Set motor direction to clockwise.

stepper.set_full_step()

#stepper.set_half_step()
#stepper.set_quarter_step()
#stepper.set_eighth_step()

# Do some steps.

home = 0
direction = cw

for j in range(0,1):

    if (j%2 == 0):
	direction = cw
    else:
	direction = ccw

    stepper.set_direction(direction)	

    for i in range(0,100):
        stepper.step()
	print i
	if (direction == cw):
	    home += 1
	elif (direction == ccw):
	    home -= 1
	
    time.sleep(1)

def goHome(homepos):

    delay_new = 0.005
    stepper.set_delay(delay_new)
    if (homepos >= 0):
	direction = ccw
    else:
	direction = cw
    stepper.set_direction(direction)

    for i in range(0, homepos):
	stepper.step()


#goHome(home)
# Clean up (just calls GPIO.cleanup() function.)
#stepper.disable()

stepper.finish()
