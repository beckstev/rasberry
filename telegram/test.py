import numpy as np
import time
import datetime as dtime
import telepot as tp
from telepot.loop import MessageLoop

now = dtime.datetime.now()
updateid=0

def test(msg):

      chat_id = msg['chat']['id']
      command = msg['text']      
      print('Naricht erkannt')

      if command == '/test':
            response= piBot.getUpdates()
            #print(response['message']['from']['username'])
            print(msg['chat']['username'])
            piBot.sendMessage(chat_id,str('TEST NARICHT') )

      if command == 'name':
            user_id=msg['id']
            user_name


piBot = tp.Bot('533241039:AAHWKO_Iobo665OK-ffCKqW80Q6RiU4yFpM')
MessageLoop(piBot, test).run_as_thread()

print('Start')

while True:
      
      time.sleep(1)
