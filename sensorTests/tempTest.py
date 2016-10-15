import Adafruit_DHT
import RPi.GPIO as GPIO
import time

sensor = Adafruit_DHT.DHT11

GPIO.setmode(GPIO.BOARD)

pine = 22

print ("Reading values")

while (1):
	hum, temp = Adafruit_DHT.read_retry(sensor, pine)
	if hum is not None and temp is not None:
		print ("Temp = {0:0.1f} and Hum = {1:0.1f}\n").format(temp, hum);
		time.sleep(5)
	else:
		print ("Retrieve Failed")
