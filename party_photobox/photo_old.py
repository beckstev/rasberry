import numpy as np
import time
import RPi.GPIO as GPIO
from sh import gphoto2 as gp
import numpy as np
import os
from pynput.keyboard import Listener

#Status LED
ReadyPin = 37 # This Led will glow, when we are ready to take a photo
PhotoPin = 35 # This Led glows when we taking the phot
SwitchPin = 33 # Switch to take a photo


def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(ReadyPin, GPIO.OUT)    # input mode
    GPIO.setup(PhotoPin, GPIO.OUT)
    GPIO.setup(SwitchPin,GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.output(PhotoPin, False)
    GPIO.output(ReadyPin,True)
    return 0


def take_a_photo():
    GPIO.output(PhotoPin, True)
    GPIO.output(ReadyPin,False)

    with open('filenumber.txt', 'r') as f:
        max_file_number = float(f.read())

    max_file_number += 1

    gp( '--capture-image-and-download' ) #takeing a photo
    print('rename')

    os.rename( 'capt0000.jpg', 'photobox_' + str(int(max_file_number)) + '.jpg') #rename file
    print('photo saved')

    
    np.savetxt('filenumber.txt', [max_file_number])

    GPIO.output(PhotoPin, False)
    GPIO.output(ReadyPin,True)
    return 0

def destroy ():
    GPIO.cleanup()

def on_press(key):
    print('Key',key)    

    if str(key) == "u'.'":
        print('Take a Photo\n')
        take_a_photo()
    else:
        print('nichts')
        pass


##Change Folder
os.chdir("/home/pi/rasberry/party_photobox/photo_folder")

## Let's take some pictures!!
setup()
while True:

	try:    
    		with Listener( on_press=on_press,) as listener:
        		listener.join()
	except:
    		destroy()
