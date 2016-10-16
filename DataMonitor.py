import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import RawObject
import json
import datetime
import os

#Saves data as filename at path, checking if path exists and
#creating it if doesn't
def saveData (filename,path,data):
        if os.path.isdir (path):
                file = open (path +"/" + filename,"w")
                file.write (data)
                file.close
        else:
                os.mkdir (pathToData)
                saveData (filename,
                          path,data)


GPIO.setmode(GPIO.BOARD)
rainSensorPine = 11
tempSensor = Adafruit_DHT.DHT11
tempSensorPine = 22
refresh = 1

pathSaveData = os.path.expanduser ("~") +"/SensorData"

print ("Aeolus Data Monitor\n")
print ("Reading values from Sensors")

while (1):
	hum, temp = Adafruit_DHT.read_retry(tempSensor, tempSensorPine)
    ## When GPIO 11 goes to 0, it detected a rain drop
    rain = not GPIO.input(rainSensorPine)

	if hum is not None and temp is not None:



        print dataobject.getJsonData()

		print ("Temp = {0:0.1f} and Hum = {1:0.1f}\n").format(temp, hum);

        ## Create RawObject
        rawdata = {
                "temp" : temp,
                "hum" : hum,
        }
        ## RawObject gets created
        dataobject = RawObject.RawObject (rawdata,"DHT11",unicode(
                datetime.datetime.now()
                .strftime("%Y-%m-%d %H:%M:%S")))
        ## Data gets saved at ~/SensorData
        saveData (dataobject.getDate() + ".json",
                  pathSaveData, dataobject.getJsonData() )
        ## Sender will be launched at another thread. Will

	else:
		print ("Temp/Hum Retrieve Failed")

	time.sleep(60)
