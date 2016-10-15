import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.IN)

while(1):
	state = GPIO.input(11);
	if (state == 0):
		print("Water of Love")
	time.sleep(0.5)
