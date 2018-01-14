import telepot as tp
from telepot.loop import MessageLoop
import time
import RPi.GPIO as GPIO

MotorPin1   = 11    
MotorPin2   = 12    
MotorEnable = 13 



def setup(): # Setup your GPIO
	GPIO.setmode(GPIO.BOARD)          # Numbers GPIOs by physical location
	GPIO.setup(MotorPin1, GPIO.OUT)
	GPIO.setup(MotorPin2, GPIO.OUT)
	GPIO.setup(MotorEnable, GPIO.OUT)
	GPIO.output(MotorEnable, GPIO.LOW)

	

def get_ID(): 
      try:
            with open ('ID.txt', 'r') as f:
                  bot_ID = f.readline()[:-1] # [:-1] to cut '\n' 
                  
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
            spin(chat_id)

      elif command == '/spinoff':
            spin_off(chat_id)

      elif command == '/hi':
           piBot.sendMessage(chat_id , str('Hi ') + chat_name + str('\n Nice to meet you !') )

      else:
            piBot.sendMessage(chat_id , 'Excuse me. \n I am not allowed to answer on your request.')
      

def spin(chat_id):
      
      GPIO.output(MotorEnable, GPIO.HIGH) # motor driver enable
      GPIO.output(MotorPin1, GPIO.HIGH)  # clockwise
      GPIO.output(MotorPin2, GPIO.LOW)
      print('Spin')

      piBot.sendMessage(chat_id , 'It is spinning. Damn that Rotor is fast.')


def spin_off(chat_id):

      GPIO.output(MotorEnable, GPIO.LOW)
      print('Spin End')
      piBot.sendMessage(chat_id , 'It stopping.')
      
      

piBot = tp.Bot( get_ID() )

setup() #Start your GPIO

try:
      print('start')
      MessageLoop(piBot, work).run_as_thread() # Start the Telegramm chat

      while True:
            time.sleep(1)

except KeyboardInterrupt:
      GPIO.output(MotorEnable, GPIO.LOW)
      GPIO.cleanup()
      



            



