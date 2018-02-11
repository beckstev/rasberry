import time
import phue
import RPi.GPIO as GPIO
import logging
logging.basicConfig()



SwitchPin = 7

RoAPin = 11    # pin11
RoBPin = 12    # pin12
RotatePin = 13



def get_IP():
      bridge_ip=0
      with open ('ip.txt', 'r') as f:
                  bridge_ip = f.readline()[:-1] # [:-1] to cut '\n'
      return bridge_ip


def connect( bridge_IP ):
      b = phue.Bridge( bridge_IP )
      b.connect()
      return b

def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(RoAPin, GPIO.IN)    # input mode
	GPIO.setup(RoBPin, GPIO.IN)
	GPIO.setup(SwitchPin,GPIO.IN, pull_up_down=GPIO.PUD_UP)
            

def on_off(ev = None):
      print('Switch switch')
      status = b.get_light(1, 'on')
      b.set_light(1,'on', not status)

def bright( rotate_level):
      print('bright', rotate_level)
      current_bright = b.get_light(1, 'bri')
      if 1<= current_bright + rotate_level <= 254:
            b.set_light(1,'bri', current_bright + rotate_level)
      elif current_bright + rotate_level > 254:
            b.set_light(1,'bri', 254)

      elif current_bright + rotate_level < 1:

            b.set_light(1,'bri', 1)
      else:
            None

def rotate(status_B):
    counter =0
    last_status_b = GPIO.input(RoBPin)
    Flag =1
    current_b_status = GPIO.input(RoBPin)
    while(not GPIO.input(RoAPin)):
          current_b_status = GPIO.input(RoBPin)
          Flag = 1        
    if Flag == 1:
          Flag =0 
          if (last_status_b == 0) and ( current_b_status == 1):
                  bright(5)
          if (last_status_b == 1) and (current_b_status == 0):
                bright(-5)
 
    return last_status_b

      
def work():
      GPIO.add_event_detect(SwitchPin, GPIO.FALLING, callback=on_off, bouncetime=200)       
      status_B = GPIO.input(RoBPin)
      while True:
            print(status_B)
            new_status_b=rotate(status_B)
            status_B = new_status_b
      

      
      

b = connect( get_IP() )
Last_RoB_Status = 0
b.set_light(1, 'on', True)
try:
    setup()
    work()
except KeyboardInterrupt: 

    GPIO.cleanup()
      
