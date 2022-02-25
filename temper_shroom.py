#!/usr/bin/python
# scp C:\GIT\Rasp\temper_shroom.py pi@192.168.178.172:~

import sys

import Adafruit_DHT


import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


sensor = 22
dhtpin = 27 
pinList = 2
PauseTimeS = 5*60
rechecktime = 10
lower_bound = True

lowtemp = 21
hightemp = 24


magicnumber = 42
fails = 0 
while magicnumber > 1:

  humidity, temperature = Adafruit_DHT.read_retry(sensor, dhtpin)

  # Un-comment the line below to convert the temperature to Fahrenheit.
  # temperature = temperature * 9/5.0 + 32

  # Note that sometimes you won't get a reading and
  # the results will be null (because Linux can't
  # guarantee the timing of calls to read the sensor).
  # If this happens try again!
  if humidity is not None and temperature is not None:
      print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
      fails = 0
  else:
      fails = fails+1
      print('Failed '+fails+' Times to get reading. Try again!')


  if fails > 100:
      print ("  Connection failed")
      magicnumber = 45

 
  if temperature < lowtemp:
      lower_bound = True



  if temperature < hightemp and lower_bound == True:
    GPIO.setup(2, GPIO.OUT)
    #    GPIO.output(i, GPIO.HIGH)


    # main loop

    try:
      GPIO.output(2, GPIO.LOW)
      print ("ON")
      print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
      print('Heizelement unter Strom ')



    # End program cleanly with keyboard
    except KeyboardInterrupt:
      print ("  Quit")

      # Reset GPIO settings
      GPIO.cleanup()


  if temperature >= hightemp:
          GPIO.setup(2, GPIO.OUT)
          #    GPIO.output(i, GPIO.HIGH)

          lower_bound = False

          # main loop

          try:
            GPIO.output(2, GPIO.HIGH)
            print ("OFF")
            print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
            print('Heizelement deaktiviert ')
            time.sleep(rechecktime)



          # End program cleanly with keyboard
          except KeyboardInterrupt:
            print ("  Quit")

            # Reset GPIO settings
            GPIO.cleanup()
            

  time.sleep(rechecktime)

GPIO.cleanup()

# End program cleanly with keyboard
#except KeyboardInterrupt:
#  print ("  Quit")

  # Reset GPIO settings
#  GPIO.cleanup()

