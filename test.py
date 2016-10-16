import datetime
import os
import RawObject
import datetime

def savedata (filename,path,data):
        file = open (path +"/" + filename,"w")
        file.write (data)
        file.close

def main():
    rawdata = {
        "temp" : 50,
        "hum" : 70
    }
    rawobj = RawObject.RawObject (rawdata,"DHT11",
                                  unicode (datetime
                                           .datetime
                                           .now()
                                           .strftime
                                           ("%Y-%m-%d %H:%M:%S")))

    pathToData = os.path.expanduser ("~") + "/SensorData"
    if os.path.isdir (pathToData):
        savedata (rawobj.getDate() + ".json",
                  pathToData,rawobj.getJsonData())
    else:
       os.mkdir (pathToData)
       savedata (rawobj.getDate() + ".json",pathToData,rawobj.getJsonData())

if __name__ == "__main__":
    main()
