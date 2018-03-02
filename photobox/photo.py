import numpy as np
import time
import RPi.GPIO as GPIO
from sh import gphoto2 as gp


last_name = 0
def setup():



def take_a_photo(last_name):
    last_name += 1
    gp( '--capture-image-and-download --filename ' + 'last_name')
    print('photo saved')
    return 0

take_a_photo()
