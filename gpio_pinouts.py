#!/usr/bin/env python
#
import RPi.GPIO as GPIO
#import time
#GPIO pins that can be used: 8, 10, 12, 16, 18, 22, 24, 26
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12,GPIO.OUT) #red led
GPIO.setup(16,GPIO.OUT) #blue led
GPIO.setup(18,GPIO.OUT) #yellow led

#LED on
#GPIO.output(18,GPIO.HIGH) #
#time.sleep(1)

#LED off
#GPIO.output(18,GPIO.LOW)

#green = blue + yellow equal
#cyan = blue 75% & yellow 25%
#white = all 3 on

red = GPIO.PWM(12, 50)
blue = GPIO.PWM(16, 50)
yellow = GPIO.PWM(18, 50)

'''
Everything @ 100% 
'''
#to get red:
red.start(100)
blue.stop()
yellow.stop() 

#to get blue:
red.stop()
blue.start(100)
yellow.stop() 

#to get yellow:
red.stop()
blue.stop()
yellow.stop(100)

#to get cyan:
red.stop()
blue.start(75)
yellow.start(25)

#to get green:
red.stop()
blue.start(100) 
yellow.start(100)

#to get white:
red.start(100)
blue.start(100) 
yellow.start(100)


'''
TO DIM without turning off:
'''
#dim red
red.ChangeDutyCycle(25)   # change the duty cycle to 90%  
#dim blue
blue.ChangeDutyCycle(25)   # change the duty cycle to 90%  
#dim yellow
yellow.ChangeDutyCycle(25)   # change the duty cycle to 90%  
  
GPIO.cleanup()
