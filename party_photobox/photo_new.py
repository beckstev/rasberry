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


def take_a_photo(Cursor,Connection):
    GPIO.output(PhotoPin, True)
    GPIO.output(ReadyPin,False)

    try: 
        Cursor.execute(""" SELECT max(Image_Number) FROM image_taken""")
        max_file_number = Cursor.fetchall()[0][0]
    
    except sq.OperationalError:
        baseCursor.execute(""" CREATE TABLE image_taken(Image_Number SMALLINT ,Time_Stampt TEXT)""")
        Connection.commit()
        max_file_number = 0
        pass
   
    max_file_number += 1

    gp( '--capture-image-and-download' ) #takeing a photo
    print('rename')

    os.rename( 'capt0000.jpg', 'photobox_' + str(int(max_file_number)) + '.jpg') #rename file
    print('photo saved')

    Cursor.execute("""INSERT INTO image_taken VALUES({}, {})""".format(max_file_number,dtime.datetime.now().time().strftime("%H:%M")) )
    Connection.commit()

    GPIO.output(PhotoPin, False)
    GPIO.output(ReadyPin,True)
    return 0

def destroy ():
    GPIO.cleanup()

def on_press(key,Cursor,Connection):
    print('Key',key)    

    if str(key) == "u'.'":
        print('Take a Photo\n')
        take_a_photo(Cursor,Connection)
    else:
        print('nichts')
        pass


##Change Folder
os.chdir("/home/pi/rasberry/party_photobox/photo_folder")
connection_number_log = sq.connect('image_taken.dat')
image_numberCursor = connection_number_log.cursor()


## Let's take some pictures!!
setup()
while True:

	try:    
    		with Listener( on_press=on_press,) as listener: ##Hier muss ich noch den Datenbankcursor übergeben.
        		listener.join()
	except:
    		destroy()

## Verwende eine Sqlite Datenbank anstatt das Textdokument, um Maximale Bilderzahl zu zuspeicher und auch später zu verwenden
## Generell muss noch angepasst werden, wo die Bilder gespeichert werden.