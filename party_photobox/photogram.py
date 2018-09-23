# -*- coding: utf-8 -*-
import telepot as tp
from telepot.loop import MessageLoop
import numpy as np
import os
import time
import datetime as dtime

now = dtime.datetime.now()
updateid=0
	

def get_ID(): 
      try:
            with open ('ID.txt', 'r') as f:
                  bot_ID = f.readline()[:-1] # [:-1] to cut '\n'
                  print('ID', bot_ID)
                  
                  if bot_ID == '\n':
                        print('No ID included in ID.txt')
                  else:
                        return bot_ID
    
      except IOError:
             print('No file found with the name ID.txt')


def send_image(msg):

    
    
    command = msg['text']
    chat_id = msg['chat']['id']
    chat_name =  msg['chat']['username']
    
    print(chat_id)

    try:
        image_name_number = command.split()            
     
    except Exception as e:
        #Mesage User
        piBot.sendMessage(chat_id, str('Es ist leider ein Fehler aufgetreten. Steven wird benachrichtigt.'))
        #Message Admin
        piBot.sendMessage(chat_id, str('Es gab einen Fehler beim splitten der User-Nachricht. Der Fehler lautet: ' + str(e) + '. \n Erzeugt wurde der Fehler von: ' + str(chat_name)))                  
        print('Hat nicht geklappt', e)
        
    if (image_name_number[0] == u'image') &  (type(int(image_name_number[1])) == type(int(7))):
            piBot.sendMessage(chat_id,str('Du erhälst Bild ') + str(image_name_number[1]) )
            piBot.sendPhoto(chat_id, photo=open('./photobox_' + str(image_name_number[1]) + '.jpg', 'rb'))
            piBot.sendMessage(chat_id, str('Es gab einen Fehler beim splitten der User-Nachricht. Der Fehler lautet: ' + str('e') + '. \n Erzeugt wurde der Fehler von: ' + str(chat_name)) )
           
        #Welcher Nummer
        #Bild schicken
        #richtiges Verzeichnis wählen
        # UserId und timestamp speichern
        # Und welches Bild die haben wollten

    elif command == '/help':
        pass
        # Liste mit user Befehlen

    elif command == '/stats':
        pass
        # Admin abfrage
        # Liste mit gespeicherten User-ID speichern, eventuell als Histogramm schicken
        # timestamps

    else:
        pass
        #Ups das war woll nichts
    
piBot = tp.Bot( get_ID() )


global admin_id
admin_id = np.genfromtxt('admin_id.txt',unpack = True)
print(admin_id)

os.chdir("/home/pi/rasberry/party_photobox/photo_folder")
try:
      
      MessageLoop(piBot, send_image).run_as_thread() # Start the Telegramm chat
      print('start')
      while True:
            time.sleep(1)

except KeyboardInterrupt:
      print('Programm wird beendet')
