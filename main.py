import light as l
import time
import RPi.GPIO as gpio
import threading
import easydriver as ed
import signal, sys
from Adafruit_ADS1x15 import ADS1x15
import numpy 
import matplotlib.pyplot as plt

pin_switch = 26 
pin_light = 13
pin_step = 24 #Yellow
delay = 0.01
pin_direction = 23 #Orange
pin_ms1 = 20 #Blue
pin_ms2 = 21 #Teal
#brown is ground

#pin_enable = 25
#pin_reset = 22

is_light_on = False
cw = True
ccw = False

switch = l.light(pin_switch, pin_light)
stepper = ed.easydriver(pin_step, delay, pin_direction, pin_ms1, pin_ms2)

HOME_POS = 0
ADS1115 = 0x01	# 16-bit ADC
adc = ADS1x15(ic=ADS1115)

'''Arguments to pass or set up after creating the instance.

Step GPIO pin number.
Delay between step pulses in seconds.
Direction GPIO pin number.
Microstep 1 GPIO pin number.
Microstep 2 GPIO pin number.
Sleep GPIO pin number.
Enable GPIO pin number.
Reset GPIO pin number.
Name as a string.'''


#def signal_handler(signal, frame):
    #print 'You pressed Ctrl+C!'
    #sys.exit(0)
#signal.signal(signal.SIGINT, signal_handler)


# Initialise the ADC using the default mode (use default I2C address)
# Set this to ADS1015 or ADS1115 depending on the ADC you are using!

# Read channels 2 and 3 in single-ended mode, at +/-4.096V and 250sps
#volts2 = adc.readADCSingleEnded(2, 4096, 250)/1000.0
#volts3 = adc.readADCSingleEnded(3, 4096, 250)/1000.0

# Now do a differential reading of channels 2 and 3

def read_Diff(sample_num=10, sps=250):
    tot_volts = []
    num_samples = sample_num
    #start_time = time.time()
    for n in range(0,num_samples): 
        voltsdiff = adc.readADCDifferential01(6144, sps)/1000.0
        tot_volts.append(voltsdiff)
        #print "%.8f" % (voltsdiff)
    #end_time = time.time()
    #elapsed_time = end_time - start_time
    
    return numpy.mean(tot_volts)
    #print elapsed_time

# Display the two different reading for comparison purposes
#print "%.8f %.8f %.8f %.8f" % (volts2, volts3, volts3-volts2, -voltsdiff)

def light_Switch(request):
    global is_light_on
    if request == "LIGHT ON":
        gpio.output(switch.pin_light1, True)
        print("Light is now on")
	is_light_on = True
    elif request == "LIGHT OFF":
        gpio.output(switch.pin_light1, False)
        print("Light is now off")
        is_light_on = False

def do_Steps(num_steps,direction=True, new_delay=0.05, ms=1):
    #print(direction, num_steps, new_delay, ms)
    global HOME_POS
    global delay
    delay = float(new_delay)
    #print(direction, num_steps, new_delay, ms)
    stepper.set_direction(direction)
    stepper.set_delay(delay)
	   
    if ms == 1:
        stepper.set_full_step()
    elif ms == 2:
        stepper.set_half_step()
    elif ms == 4:
        stepper.set_quarter_step()
    elif ms == 8:
        stepper.set_eighth_step()
    else:
	stepper.set_full_step()

    for i in range(0,num_steps):
        stepper.step()
        if direction == True:
            HOME_POS += 1
        elif direction == False:
            HOME_POS -= 1
    
def go_Home():
    global HOME_POS
    print HOME_POS

    stepper.set_delay(0.05)
    if HOME_POS >= 0:
	stepper.set_direction(ccw)
    if HOME_POS < 0:
	stepper.set_direction(cw)	
    for i in range(0, HOME_POS):
	stepper.step()
    HOME_POS = 0
    #print "New home=" + str(HOME_POS)

def button():
    blink=True
    global is_light_on

    while True:
        time.sleep(0.01)
        if is_light_on == False or is_light_on == None:
	    if (gpio.input(switch.pin_switch_out) == 1):
                gpio.output(switch.pin_light1, False)
            elif (gpio.input(switch.pin_switch_out) == 0):
		if blink: 
		    gpio.output(switch.pin_light1, True)
		    blink = False
		    time.sleep(0.5)
		elif blink == False:
		    gpio.output(switch.pin_light1, False)
		    blink = True
		    time.sleep(0.5)

def start_Butthread():
    button_thread = threading.Thread(target=button,)
    button_thread.daemon = True
    button_thread.start()

def do_Obs(data_points=200,delay=0.05,samples_per_step=40,sps=860):
    global HOME_POS 
    volts_data = []
    position_data = []
    
    for i in range(data_points):
	volts_data.append(read_Diff(samples_per_step,sps))
	time.sleep(0.5)
	do_Steps(1)
	position_data.append(HOME_POS)
	
    plt.plot(position_data, volts_data)
    plt.xlabel("Relative Position")
    plt.ylabel("Intensity")
    
    plt.savefig("TestPlot.png")
    plt.cla()

def calibrate():
    global HOME_POS
    """threshold_intensity = 2.0
    while True: 
        intensity = read_Diff(20)
        if intensity < threshold_intensity:
	    do_Steps(1)
	else:
	    HOME_POS = 0
	    while True:
		intensity = read_Diff(20)
		if intensity > threshold_intensity:
		    do_Steps(1)
		else:
		    HOME_POS = HOME_POS / 2
		    go_Home()
		    break
	    break"""
    while gpio.input(switch.pin_switch_out) == 1:
	do_Steps(1)
    HOME_POS = 0

def user_Input():
    try:   
        prompt = ""	
 
        while prompt != "STOP":
            prompt = raw_input("Main Menu.  Available commands:\nLight on,\nLight off,\nDo steps,\nGo obs,\nGo home,\nCalibrate,\nStop \n:")
            prompt = prompt.upper()
        
            if prompt[0:5] == "LIGHT":
	        light_Switch(prompt)
		
	    if prompt == "STOP":	    
	        switch.finish()
	     
            if prompt == "DO STEPS":
	        dir = None
	        ms = None
            	dly = None
	        while (dir!="cw") and (dir!="ccw"):
		    dir = raw_input("Direction (cw or ccw): ")
	        steps = int(raw_input("Number of steps: "))
	        while (ms != 1) and (ms != 2) and (ms != 4) and (ms != 8):
		    ms = int(raw_input("Microsteps(1,2,4,8): "))
	        while dly <= 0:
		    dly = float(raw_input("Delay: "))
	        #print type(dly)
	        if dir == "cw":
		    dir_ = cw
	        elif dir == "ccw":
		    dir_ = ccw
	        do_Steps(steps, dir_, dly, ms)

	    if prompt == "CALIBRATE":
		calibrate()

	    if prompt == "GO HOME":
	        go_Home()		

	    if prompt == "DO OBS": 
		do_Obs()
		
	   
    except KeyboardInterrupt:
        switch.finish()

if __name__ == "__main__":
    start_Butthread()
    user_Input()

