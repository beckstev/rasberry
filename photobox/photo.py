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
    GPIO.output(PhotoPin, False)
    GPIO.output(ReadyPin,True)
    return 0


def take_a_photo(max_file_number):
    GPIO.output(PhotoPin, True)
    GPIO.output(ReadyPin,False)

    max_file_number += 1
    np.savetxt('filenumber.txt', [max_file_number])

    gp( '--capture-image-and-download' ) #takeing a photo
    
    os.rename( 'capt0000.jpg', 'photobox_' + str(int(max_file_number)) + '.jpg') #rename file
    print('photo saved')

    GPIO.output(PhotoPin, False)
    GPIO.output(ReadyPin,True)
    return 0

def destroy ():
    GPIO.cleanup() 


##Change Folder
os.chdir("/home/pi/rasberry/photobox/photo_folder")

max_file_number = 0

with open('filenumber.txt', 'r') as f:
    max_file_number = float(f.read())

print( type(max_file_number), max_file_number)
## Let's take some pictures!!
setup()
time.sleep(5)
try:
    take_a_photo(max_file_number)
except:
    destroy()
