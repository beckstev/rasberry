# -*- coding: utf-8 -*-
import telepot as tp
from telepot.loop import MessageLoop
import numpy as np
import os
import time
import datetime as dtime
import sqlite3 as sq


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


class PiPhotobox(path_to_admin_id):

    def __init__(self, path_to_admin_id):
         
        self.admin_id = np.genfromtxt(path_to_admin_id,unpack = True)
        self.connection_user_log = sq.connect('user_log.dat')
        self.connection_number_log = sq.connect('image_taken.dat')
        
        self.baseCursor = connection_user_log.cursor()
        self.image_numberCursor = connection_number_log.cursor()


    def end_connection(self):
      
        self.connection_user_log.close()
        self.connection_number_log.close()


    ##########################################################################################################################
    ### Function to generated a Bar plot, thats shows which user requested how many images ###################################
    ##########################################################################################################################
    def name_downloads_statistic(self,chat_id):
      self.baseCursor.execute(""" SELECT Username FROM user_log""")
      
      ### Generate the data
      name_list = []
      number_list = []
      for element in Counter(self.baseCursor.fetchall()).most_common():
        name_list.append(element[0][0])
        number_list.append(element[1])
      
      ### Generate Plot
      plt.bar(name_list,number_list)
      plt.ylabel('Anzahl Downloads')
      plt.savefig('./stats/user_statisitic.jpg')
    
    
      ### Send requested Plot to the User
      piBot.sendMessage(chat_id, str('Hier die Nutzerstatistik:'))
      piBot.sendPhoto(chat_id, photo=open('./stats/user_statisitic.jpg', 'rb'))
    
      ### Close BaseCursor
      self.baseCursor.close()
      
    
      return 0
    
    ###########################################################################################################################################################################
    ### Function to generated a Histogram, which shows the how often a image was got a download request. Further, you get the image number of the two most requested images ###
    ###########################################################################################################################################################################   
    
    def most_popular_statistic(self,chat_id):
    
      self.baseCursor.execute(""" SELECT Image_Number FROM user_log""")
      
      ### Generated a List with all Imagenumber
      image_number_log = [ i[0] for i in self.baseCursor.fetchall()]
      
      ### Plot a histogramm
      plt.hist(image_number_log, bins=range(min(image_number_log), max(image_number_log) + 2, 1), rwidth=0.95 )
      plt.grid(axis='y', alpha = 0.8)
      plt.xticks(range(min(image_number_log), max(image_number_log) + 2, 1))
      plt.xlabel('Bildnummer')
      plt.ylabel('Anzahl Downloads')
      plt.savefig('./stats/number_downloads.jpg')
      
      #### Generate a list with the two most requested images ##############################################################################
      
      image_number_log_max = Counter(image_number_log).most_common(2) ## Get the number with the most requests
    
      ## Send the requested stats
      piBot.sendMessage(chat_id, 'Bildnummer: ' + str(image_number_log_max[0][0]) +' ist im Moment mit ' + str(image_number_log_max[0][1]) + ' Downloads, dass gefragteste Bild. \n'
        'Dahinter ist Bildnummer: ' + str(image_number_log_max[1][0]) + ' mit ' + str(image_number_log_max[1][1]) + ' Downloads, dass zweit gefragteste Bild.')
      
      piBot.sendMessage(chat_id, str('Hier ist die Fotonnachfragestatistik:'))
      piBot.sendPhoto(chat_id, photo=open('./stats/number_downloads.jpg', 'rb'))
    
      ### Close BaseCursor
      self.baseCursor.close()
    
      return 0
    
    
    ##########################################################################################################################
    ### Function to generated a timebased Histogram, that shows how many images were downloaded during a spezific timeslot ###
    ##########################################################################################################################
    def time_based_statistic(self,chat_id,name):
      
      if name == 'timebased':
          self.baseCursor.execute(""" SELECT Time_Stampt FROM user_log""")
          ylabel_name = 'Anzahl Downloads'
          ### Generate a int list with all the timestamps. A Stamp is formatted like this: '20:30'
          time_stampt_list = [ int(i[0].split(':')[0]) for i in self.baseCursor.fetchall()]


      elif name == 'taken':
          self.image_numberCursor.execute(""" SELECT Time_Stampt FROM image_taken""")
          ylabel_name = 'Anzahl Fotos'
          time_stampt_list = [ int(i[0].split(':')[0]) for i in self.image_numberCursor.fetchall()]

      else:
        pass

    
      ### Generated a plot
      plt.hist(time_stampt_list,  bins=range(min(time_stampt_list), max(time_stampt_list) + 2, 1), rwidth=0.95 )
      plt.xticks(range(min(time_stampt_list), max(time_stampt_list) + 2, 1))
      plt.xlabel('Uhrzeit')
      plt.ylabel(ylabel_name)
      plt.grid(axis='y', alpha = 0.8)
      plt.savefig('./stats/time_based_statistic.jpg')
    
      piBot.sendMessage(chat_id, str('Hier ist die zeitaufgelöste Statistik:'))
      piBot.sendPhoto(chat_id, photo=open('./stats/time_based_statistic.jpg', 'rb'))  
    
      ### Close BaseCursor
      self.baseCursor.close()
      return 0

    

    def send_image(self,msg):

        command = msg['text']
        chat_id = msg['chat']['id']
        chat_name =  msg['chat']['username']
        
        ### Split Command message to get the command and eventually the image_number ###
       
        command = command.split()            
        
        if (command[0] == u'image') &  (type(int(command[1])) == type(int(7))):
                
                try:
                  piBot.sendMessage(chat_id,str('Du erhälst Bild ') + str(command[1]) )
                  piBot.sendPhoto(chat_id, photo=open('./photobox_' + str(command[1]) + '.jpg', 'rb'))

                  self.baseCursor.execute("""INSERT INTO user_log VALUES({}, {}, {}, {})""".format(str(chat_name),chat_id, int(command[1]), dtime.datetime.now().time().strftime("%H:%M")) )
                  self.connection_user_log.commit()
                
                except HIERDERFEHLERDERENTSTEHTWENNDASBILDNICHTDAIST:
                  piBot.sendMessage(chat_id, 'Es exestiert kein Bild mit der Nummer' + str(command[1]) + '. Bitte versuche es nochmal.')
                  pass
                
                except sq.OperationalError:
                  
                  self.baseCursor.execute(""" CREATE TABLE user_log(Username TEXT ,User_ID SMALLINT, Image_Number SMALLINT,Time_Stampt TEXT)""")
                  
                  self.baseCursor.execute("""INSERT INTO user_log VALUES({}, {}, {}, {})""".format(str(chat_name),chat_id, int(command[1]), dtime.datetime.now().time().strftime("%H:%M")) )
                  self.connection_user_log.commit()
                  pass
                
                except Exception as e:
                  piBot.sendMessage(chat_id, 'Ein unbekannter Fehler ist aufgetreten. Steven wird benachrichtigt.')
                  piBot.sendMessage(self.admin_id, 'Es ist ein Fehler bei dem verschicken des Fotos mit der Nummer ' + str(command[1]) + ' aufgetreten. Der Fehler Code lautet: \n' + str(e)+ '.\n Auf den Fehler wird mit \pass reagiert.')
                  pass
        
        elif command[0] == u'stat':

          if command[1] == u'name':
            name_downloads_statistic(chat_id)
          
          elif command[1] == u'popular':
            most_popular_statistic(chat_id)

          elif command[1] == u'timebased':
            time_based_statistic(chat_id)

          else:
             piBot.sendMessage(chat_id, 'Leider ist deine Auswahl nicht dabei. \n Zur Verfügung stehen die Befehle: \n --- name --- : Dieser Befehl (ohne die --- ) zeigt dir an welcher User wie viel Bilder gedownloadet hat \n --- popular --- : Dieser Befehl (ohne die --- ) zeigt dir die beliebtesten Bilder \n --- timebased--- : Dieser Befehl (ohne die --- ) zeigt dir wie viele Bilder zu einer bestimmten Uhrzeit (stündlich) gedownloadet wurden \n --- taken ---: Dieser Befehl (ohne die ---) zeigt dir wie viele Bilder zu einer bestimmten Uhrzeit (stündlich) mit der Photobox aufgenommen wurden')

        elif command[0] == u'help_admin':
           piBot.sendMessage(chat_id, 'Steven wird benachritigt.')
           piBot.sendMessage(self.admin_id,'Hilfeanfrage von: ' + str(chat_name))


        else:
          piBot.sendMessage(chat_id, 'Leider ist dein Befehl nicht in der Datenbank verzeichnet. Hier nochmal deine Möglichkeiten:\n --- image image_number ---: Hier erhälst du das Bild mit der Nummer image_number direkt auf dein Handy geschickt bspw image 7, um Bildnummer 7 zuerhalten. \n --- stat keyword ---: Hier erhälst du verschiedene Nutzerstatistiken der Photobox. Als Keyword stehen zur Verfügung: name, popular, timebased und taken.Bsp: stat name \n --- help_admin ---: Hier wird Steven auf seinem Handy benachrichtigt und kommt schnellstmöglichst zu dir. Wenn er nicht kommt solltest du ihn suchen gehen.')
  
### Start Photobox if used as main class

if __name__ == '__main__':    
  piBot = tp.Bot( get_ID() )
  
  piphotobox = PiPhotobox('admin_id.txt')

  
  os.chdir("/home/pi/rasberry/party_photobox/photo_folder")
  
  try:
        
        MessageLoop(piBot, piphotobox.send_image).run_as_thread() # Start the Telegramm chat
        print('start')
        while True:
              time.sleep(1)
              
  except KeyboardInterrupt:
        print('Programm wird beendet')
        piphotobox.end_connection()




### 
# Implementierung der User_Stats Database
# Einfügen der Funktionen
# Einfügen einer KeyboardInterrupt Funtkion
# Einfügen der FotoDatabase
# mehr try Funktionen
# Erst Erstellung der User_stat Databbase
# Shot or Beer: Random werden Leute aus einer Liste ausgewählt die mit einem trinken müssen. Hierbei ist es nur möglich User zuverwenden die bereits ein Bild requested haben.