import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT)
#
GPIO.output(29, True)
time.sleep(2)
GPIO.output(29, False)
#

GPIO.cleanup()
