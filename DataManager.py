from RawObject import RawObject
from daemon import Daemon

class DataManager (Daemon):
    """Class DataManager
    Picks up data at ~/SensorData and turns it into final json endpoint
    """
    # Attributes:

    # Operations
    def storeData(self, object):
        """function storeData

        object: RawObject

        returns void
        """
        return None # should raise NotImplementedError()

    def getData(self):
        """function getData

        returns RawObject
        """
        return None # should raise NotImplementedError()

    def __connect(self):
        """function connect

        returns void
        """
        return None # should raise NotImplementedError()

    def __disconnect(self):
        """function disconnect

        returns
        """
        return None # should raise NotImplementedError()

    def __validate(self):
        """function validate

        returns
        """
        return None # should raise NotImplementedError()


