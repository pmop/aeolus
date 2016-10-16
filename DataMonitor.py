import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import RawObject
import json
import datetime
import os
from daemon import Daemon
from RawObject import RawObject


#Saves data as filename at path, checking if path exists and
#creating it if doesn't

## Setting up things

print ("Aeolus Data Monitor\n")
print ("Reading values from Sensors")

class DataMon (Daemon):
        def run(self):

                GPIO.setmode(GPIO.BOARD)
                rainSensorPine = 11
                tempSensor = Adafruit_DHT.DHT11
                tempSensorPine = 22
                refresh = 60
                GPIO.setup(11, GPIO.IN)

                pathSaveData = os.path.expanduser ("~") +"/SensorData"
                while (True):
                        hum, temp = Adafruit_DHT.read_retry(tempSensor,
                                                            tempSensorPine)
                        #Get time closest as possible to sensor read call
                        currentdate = unicode(datetime.
                                              datetime.now()
            		                          .strftime("%Y-%m-%d %H:%M:%S"))
                        rain = not GPIO.input(rainSensorPine)
                        if hum is not None and temp is not None:
                                rawDHT11 = {
                                        "temp": temp,
                                        "hum" : hum
                                }
                                rawYL83 = {
        		                        "rain" : rain
	                            }
                                dht11Object = RawObject (rawDHT11,
                                                         "DHT11",
                                                         currentdate)
                                yl83Object = RawObject (rawYL83,
                                                        "YL83",
                                                        currentdate)

                                self.__saveData
                                (dht11Object.getDate() + ".json",
                                          pathSaveData,
                                          dht11Object.getJsonData() )

                                self.__saveData
                                (yl83Object.getDate() + "C.json",
                                          pathSaveData,
                                          yl83Object.getJsonData() )
                        else:
                                print ("Couldn't retrieve information")
                time.sleep (6) # sleeps for 6 seconds

        def __saveData (self,filename,path,data):
                if os.path.isdir (path):
                        file = open (path +"/" + filename,"w")
                        file.write (data)
                        file.close
                else:
                        os.mkdir (path)
                        saveData (filename,
                                  path,data)

