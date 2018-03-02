import numpy as np
import time
import RPi.GPIO as GPIO
from sh import gphoto2 as gp
import os


last_name = 0
def setup():
    return 0


def take_a_photo(last_name):
    last_name += 1
    gp( '--capture-image-and-download' )
    os.rename( 'capt0000.jpg', 'photobox_' + str(last_name) + '.jpg') 
    print('photo saved')
    return 0


##Change Folder
os.chdir("/home/pi/rasberry/photobox/photo_folder")

## Let's take some pictures!!
take_a_photo(last_name)
