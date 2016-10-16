import paramiko
from paramiko import SSHClient
from scp import SCPClient
from daemon import Daemon
from os.path import exists, expanduser, isfile, join
from os import listdir, remove
import datetime
import time, sys
import requests

class SendData(object):
    _sshclient = None
    _scpclient = None
    #Example:
    #sender = SendData ('11.22.33.44','username')
    def __init__(self,serverip,rusername):
        self._sshclient = SSHClient()
        self._sshclient.set_missing_host_key_policy (paramiko.AutoAddPolicy())
        # Server needs to have your key
        self._sshclient.load_system_host_keys()
        self._sshclient.connect (hostname=serverip,username=rusername)
        self._scpclient = SCPClient (self._sshclient.get_transport ())
        #Example: send (pathtofile)
    def send (self,file,remotepath='.'):
        success = False
        status = "01 Didn't do anything"
        try:
            transport = self._sshclient.get_transport()
            transport.send_ignore()
            self._scpclient.put (file,remote_path=remotepath)
            success = True
            status = "00 OK"
        except EOFError, e:
            success = False
            status = "02 No connection"
        return success,status

    def end (self):
        self._scpclient.close()


## Sender daemon
class Sender(Daemon):
#class Sender(object):
    def run(self):
        log = []
        isCon = self.__checkConnection()
        con = None
        while (True):
            sent = []
            toSend = self.__listData()
            # Inits ssh if has connection
            if isCon and con == None:
                con = SendData ('159.203.103.181','aeolus')

            for file in toSend:
                success = False
                status = "No connection"
                if isCon and con != None:
                    success,status = con.send (file,"~/SensorData")
                if success:
                    sent.append (file)
                    log.append (self.__timeNow() +  " " +
                                       status + " " + file)
                else:
                    mesg = "Couldn't send " + status + " "
                    log.append (self.__timeNow() + mesg  + file)
                    isCon = self.__checkConnection()
                    if isCon:
                        con = SendData ('159.203.103.181','aeolus')

            self.__wipeSentData (sent)
            self.__writeToLog (log)
            time.sleep (1)
            if len(log) > 0:
                log[:] = []

    def __checkConnection (self,url='http://www.google.com',timeout=5):
        try:
            _ = requests.get (url,timeout=timeout)
            return True
        except requests.ConnectionError:
            return False

    def __listData(self):
        print "listing files"
        dir =  expanduser("~") + "/SensorData"
        files = None
        if exists(dir):
            files = [join(dir,f) for f in listdir(dir) if isfile(join(dir,f)) ]
        return files

    def __timeNow(self):
        return unicode(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def __wipeSentData(self,fileList):
        print "wiping files"
        for file in fileList:
            if isfile(file):
                remove(file)

    def __writeToLog(self,log):
        print "logging proc"
        dir = expanduser ("~")
        file = open (join (dir,"SENDERLOG"),"a")
        for str in log:
            file.write (str+"\n")
        file.close ()

def main ():
    daemon = Sender('/tmp/dsender.pid')
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
