import time
import phue
import RPi.GPIO as GPIO

SwitchPin = 7

RoAPin = 11    # pin11
RoBPin = 12    # pin12



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

def bright( roate_level):
      current_bright = b.get_light(1, 'bri')
      if 1<= current_bright + rotate_level <= 254:
            b.set_light(1,'bri', bright_value + rotate_leve)
      elif current_bright + rotate_level > 254:
            b.set_light(1,'bri', 254)

      elif current_bright + rotate_level < 1:
            b.set_light(1,'bri', 1)
      else:
            None

def rotate():
      Last_RoB_Status = GPIO.input(RoBPin)
      while(not GPIO.input(RoAPin)):
		Current_RoB_Status = GPIO.input(RoBPin)
		flag = 1
	if flag == 1:
		flag = 0
		if (Last_RoB_Status == 0) and (Current_RoB_Status == 1):
			globalCounter = globalCounter + 1
			print 'globalCounter = %d' % globalCounter
		if (Last_RoB_Status == 1) and (Current_RoB_Status == 0):
			globalCounter = globalCounter - 1
			
      
      
def work():
      GPIO.add_event_detect(SwitchPin, GPIO.FALLING, callback=on_off, bouncetime=200)
      
      while True:
            time.sleep(1)
      

      
      

b = connect( get_IP() )

Last_RoB_Status = 0

bright(1)
setup()
work()
      

      
