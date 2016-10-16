import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import RawObject
import json
import datetime
import os
from daemon import Daemon
from RawObject import RawObject


## Setting up things
print ("Aeolus Data Monitor\n")
print ("Reading values from Sensors")

class DataMon (Daemon):
        __delay = 6
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
                                time.sleep (self.__delay) # sleeps for 6 seconds

        def __saveData (self,filename,path,data):
                if os.path.isdir (path):
                        file = open (path +"/" + filename,"w")
                        file.write (data)
                        file.close
                else:
                        os.mkdir (path)
                        saveData (filename,
                                  path,data)

def main ():
    daemon = DataMon ('/tmp/dsender.pid')
  #  dsender = Sender()
 #   dsender.run ()
  #  dsender.stop ()
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
if __name__ == "__main__":
    main()
