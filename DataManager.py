from RawObject import RawObject
from daemon import Daemon
from os.path import expanduser, exists, isfile, join, split
from os import listdir, rename, mkdir
import json

class DataManager (object):
    __pathToData = None
    __xAxisKeys = []
    __yAxisKeys = []
    #def __init__(self,pidfile):
       #Daemon.__init__(self,pidfile=pidfile)
    def __init__(self):
        self.__pathToData = expanduser ("~") + "/SensorData"

    def __listFiles(self):
        print "listing files"
        dir =  self.__pathToData
        files = None
        if exists(dir):
            files = [join(dir,f)
                     for f in listdir(dir) if isfile(join(dir,f)) ]
        return files

    def setDataPath(self,path):
        self.__pathToData (path)

    def setXAxisKeys (self,keylists):
        self.__xAxisKeys = keylists

    def appendXAxisKey (self,key):
        self.__xAxisKeys.append (key)

    def setYAxisKeys (self,keylists):
        self.__yAxisKeys = keylists

    def appendYAxisKey (self,key):
        self.__yAxisKeys.append (key)
    # Either generates or appends to endpoint
    def __appendToAxis(self, axis,key, value):
        dir = expanduser ("~") + "/endpoints"
        dir = join (dir,key+".json")
        if exists(dir) and isfile (dir):
            file = open (dir,"r")
            data = json.load (file)
            file.close ()
            data["data"][0][axis].append (value)
            file = open (dir,"w")
            file.write (json.dumps (data) )
            file.close ()

    def updateData (self):
        self.generateBaseEndpoints ()
        dir = expanduser ("~") + "/endpoints"

        keyToFile = dict()
        for key in self.__yAxisKeys:
            keyToFile[key] = join (dir,key)

        filedone = []
        listFiles = self.__listFiles()
        for file in listFiles:
            filedone.append (file)
            with open (file) as data_file:
                data = json.load (data_file)
                for key in self.__yAxisKeys:
                    value = data["rawData"].get(key)
                    self.__appendToAxis ('x',key,data["date"])
                    if value is not None:
                        self.__appendToAxis ('y',key,value)
            data_file.close ()

        self.__mvData (filedone)

    def __mvData(self,fileList):
        procddir = join(self.__pathToData,"procd")
        if exists (procddir) and not isfile (procddir):
            for file in fileList:
                #splits filepath into head=path, tail=name
                head, tail = split (file)
                # Moves file to proccdir
                rename (file,join(procddir,tail))
        else:
            mkdir (procddir)
            self.__mvData (fileList)

    def generateBaseEndpoints (self):

        #fileList = self.__listFiles()
        dir = expanduser ("~") + "/endpoints"
        # Dict of keys -> files that will be generated
        basefiles = dict()
        for key in self.__yAxisKeys:
            if not exists (join (dir,key) ):
                basefiles[key] = join(dir,key)
        print basefiles
        if len (basefiles) > 0:
            endpoints = dict()
            for yAxisKey in self.__yAxisKeys:
                f = open (basefiles[yAxisKey]+".json","w")
                endpoints[yAxisKey] = {
                    "data": [
                        {
                            "type": "scatter",
                            "mode": "lines",
                            "x": [
                            ],
                            "y": [
                            ],
                            "line": {
                                "width": 1
                            },
                            "error_y": {
                                "array": [
                                ],
                                "thickness": 0.5,
                                "width": 0
                            }
                        }
                    ],
                    "layout": {
                        "yaxis": {
                            "title": yAxisKey
                        },
                        "xaxis": {
                            "showgrid": "false",
                            "tickformat": "%B, %Y"
                        },
                        "margin": {
                            "l": 40,
                            "b": 10,
                            "r": 10,
                            "t": 20
                        }
                    }
                }
                f.write (json.dumps (endpoints[yAxisKey]))
                f.close ()

def main():
    test = DataManager ()
    test.setYAxisKeys (["hum","temp"])
    test.updateData()


if __name__ == "__main__":
    main()
