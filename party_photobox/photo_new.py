import time
import RPi.GPIO as GPIO
from sh import gphoto2 as gp
import os
from pynput.keyboard import Listener
import datetime as dtime
import sqlite3 as sq

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

    try: 
        image_numberCursor.execute(""" SELECT max(Image_Number) FROM image_taken""")
        max_file_number = image_numberCursor.fetchall()[0][0]
    except sq.OperationalError:
        image_numberCursor.execute(""" CREATE TABLE image_taken(Image_Number SMALLINT ,Time_Stampt TEXT)""")
        connection_number_log.commit()
        max_file_number = 0
        pass
   
    max_file_number += 1
    print('taking')
    gp( '--capture-image-and-download' ) #takeing a photo

    os.rename( 'capt0000.jpg', 'photobox_' + str(int(max_file_number)) + '.jpg') #rename file

    image_numberCursor.execute("""INSERT INTO image_taken VALUES({}, "{}")""".format(max_file_number,dtime.datetime.now().time().strftime("%H:%M")) )
    connection_number_log.commit()

    GPIO.output(PhotoPin, False)
    GPIO.output(ReadyPin,True)
    print('Done')
    return 0

def destroy ():
    GPIO.cleanup()
    connection_number_log.close()

def on_press(key): 

    if str(key) == "u'.'":
        take_a_photo()
    elif str(key) == "u'x'":
        Listener.stop()

        destroy()
        
    else:
        print('nichts')
        pass


##Change Folder
os.chdir("/home/pi/rasberry/party_photobox/photo_folder")

global connection_number_log
global image_numberCursor
connection_number_log = sq.connect('../stats_dats/image_taken.dat',check_same_thread=False)
image_numberCursor = connection_number_log.cursor()


## Let's take some pictures!!
setup()
while True:

	try:    
    		with Listener( on_press=on_press,) as listener:
        		listener.join()
	except KeyboardInterrupt:
    		destroy()
    		

