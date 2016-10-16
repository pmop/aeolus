import  hashlib
import json
class RawObject(object):
    """
        RawObject should encapsulate raw object data
    """
    # Attributes:
    __rawData = None  # (jsonobject)
    __MD5 = None  # (string)
    __sensorName = None  # (string)
    __date = None  # (date)

    def __init__(self, rawData, sensorName, date):
        self.__date = date
        self.__MD5 = hashlib.md5 ()
        self.__rawData = rawData
        self.__sensorName = sensorName

    # Operations
    def getRawData(self):
        """function getRawData

        returns bytearray
        """
        return self.__rawData

    def getJsonData(self):
        """function getJsonData
        returns JsonObject
        raise NotImplementedError()
        """
        data = {
            "rawData" : self.__rawData,
       #     "md5" : self.__MD5.hexdigest (),
            "date" : self.__date,
            "sensorName" : self.__sensorName
        }
        self.__MD5.update ( json.dumps(data) )
        data = {
            "rawData" : self.__rawData,
            "md5" : self.__MD5.hexdigest (),
            "date" : self.__date,
            "sensorName" : self.__sensorName
        }
        return json.dumps(data)

   # def getMD5(self):

        """function getMD5
        raise NotImplementedError()
        """
        return self.__md5.hexdigest()

    def getDate(self):
        return self.__date


