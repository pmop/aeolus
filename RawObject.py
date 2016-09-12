import  hashlib
class RawObject:
    """Abstract class RawObject
    """
    # Attributes:
    __rawData = None  # (bytearray) 
    __MD5 = None  # (string) 
    __sensorName = None  # (string) 
    __date = None  # (date)

    def __init__(self, rawData, sensorName, date):
        self.__date = date
        self.__MD5 = hashlib.md5 ()
        self.__rawData = rawData
        self.__MD5.update (rawData)
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
        """
        raise NotImplementedError()
    
    def getMD5(self):

        """function getMD5
        raise NotImplementedError()
        """
        return self.__md5.digest()

    def getDate(self):
        return self.__date


