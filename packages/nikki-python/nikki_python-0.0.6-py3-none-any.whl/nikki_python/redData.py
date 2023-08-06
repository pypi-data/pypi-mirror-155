
from dataclasses import dataclass

redataInfoEnum_OK = "OK"
redataInfoEnum_ERROR = "ERROR"


@dataclass
class dataBundle:
    name = ""  # primary key
    data = ""
    desc = ""  # tells how the data format looks like with comment
    # // ex
    # // {
    #     // a: 2, // info about the field a
    #     //}


class redData:
    def __init__(self, srvID, instID, sessionID):

        self.sessionID = sessionID
        self.data = dataBundle()
        self.msg = ""
        self.status = redataInfoEnum_OK
        self.srvID = srvID
        self.instID = instID

        # print("redData===>", self, dir(self))
