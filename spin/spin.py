import telepot as tp
from telepot.loop import MessageLoop
import time

def get_ID():
      try:
            with open ('ID.txt', 'r') as f:
                  bot_ID = f.readline()[:-1]
                  
                  if bot_ID == '\n':
                        print('No ID included in ID.txt')
                  else:
                        return bot_ID
    
      except IOError:
             print('No file found with the name ID.txt')


def work(msg):

      command = msg['text']
      chat_id = msg['chat']['id']
      chat_name =  msg['chat']['username']

      if command == '/spin':
            spin()

      if command == '/spinoff':
            spin_off()

      if command == '/hi':
           piBot.sendMessage(chat_id , str('Hi ') + chat_name + str('\n Nice to meet you !') )

      else:
            piBot.sendMessage(chat_id , 'Excuse me. \n I am not allowed to answer on your request.')
      


piBot = tp.Bot( get_ID() )


MessageLoop(piBot, work).run_as_thread()
            
print('start')

while True:
      time.sleep(1)
