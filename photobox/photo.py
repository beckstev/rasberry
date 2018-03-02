import numpy as np
import time
import RPi.GPIO as GPIO
from sh import gphoto2 as gp
import numpy as np
import os

#Status LED
ReadyPin = 37 # This Led will glow, when we are ready to take a photo
PhotoPin = 35 # This Led glows when we taking the phot
SwitchPin = 33 # Switch to take a photo


def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(ReadyPin, GPIO.OUT)    # input mode
	GPIO.setup(PhotoPin, GPIO.OUT)
	GPIO.setup(SwitchPin,GPIO.IN, pull_up_down = GPIO.PUD_UP)
    return 0


def take_a_photo(max_file_number):
    GPIO.output(PhotoPIN, True)
    GPIO.output(ReadyPIN,False)

    max_file_number += 1
    np.savetxt(filenumber.txt, last_name)

    gp( '--capture-image-and-download' )
    os.rename( 'capt0000.jpg', 'photobox_' + str(last_name) + '.jpg')
    print('photo saved')

    GPIO.output(PhotoPIN, False)
    GPIO.output(ReadyPIN,True)
    return 0


##Change Folder
os.chdir("/home/pi/rasberry/photobox/photo_folder")

max_file_number = 0

with open('filenumber.txt', 'r') as f:
    max_file_number = f.read()
## Let's take some pictures!!
take_a_photo(last_name)
