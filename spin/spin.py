import telepot as tp
from telepot.loop import MessageLoop

def get_ID():
      try:
            with open ('ID.txt', 'r') as f:
                  bot_ID = f.read()
                  if bot_ID == '\n':
                        print('No ID included in ID.txt')
                  else:
                        return bot_ID
    
      except IOError:
             print('No file found with the name ID.txt')


print(get_ID())
