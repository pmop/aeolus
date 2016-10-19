from RawObject import RawObject
from daemon import Daemon
from os.path import expanduser, exists, isfile, join, split, splitext, basename
from os import listdir, rename, mkdir
import json
import datetime
from collections import OrderedDict

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
	sfiles = sorted (files, key = lambda x:
	 datetime.datetime.strptime ( basename ( splitext(x)[0] )
		 if  basename ( splitext(x)[0] )[-1] != 'C' else
		 basename ( splitext(x)[0] )[:-1] ,
		'%Y-%m-%d %H:%M:%S') )
        return sfiles
	
    def test(self):
	self.generateBaseEndpoints()

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
		data = None
		with open (dir) as file_data:
			data = json.load (file_data)
        	    	data["data"][0][axis].append (value)

		with open (dir,"w") as file_data:
  	         	json.dump (data,fp=file_data,sort_keys=True) 

    def updateData (self):
        self.generateBaseEndpoints ()
        dir = expanduser ("~") + "/endpoints"

# prob redundant
        keyToFile = dict()
        for key in self.__yAxisKeys:
            keyToFile[key] = join (dir,key+".json")

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
            if not exists (join (dir,key + ".json") ):
                basefiles[key] = join(dir,key + ".json")
		print "creating: (doesn't exists)" + join (dir,key +".json")

        if len (basefiles) > 0:
            endpoints = dict()
            for yAxisKey in self.__yAxisKeys:
                f = open (basefiles[yAxisKey],"w")
                endpoints[yAxisKey] = OrderedDict ( {
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
			    }
                        }
                    ],
                    "layout": {
                        "yaxis": {
                            "title": yAxisKey
                        },
                        "xaxis": {
                            "showgrid": "false",
                            "tickformat": ""
                        },
                        "margin": {
                            "l": 40,
                            "b": 10,
                            "r": 10,
                            "t": 20
                        }
                    }
                } )
                json.dump (endpoints[yAxisKey],fp = f, sort_keys=True)
                f.close ()

def main():
    test = DataManager ()
    test.setYAxisKeys (["hum","temp"])
    test.updateData()


if __name__ == "__main__":
    main()
