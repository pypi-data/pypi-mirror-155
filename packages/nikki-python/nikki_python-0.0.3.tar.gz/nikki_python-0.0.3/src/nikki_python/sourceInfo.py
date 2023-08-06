
import uuid
import json

from src.redData import dataBundle, redData


class sourceInfo:

    def __init__(self):
        self.srvID = uuid.uuid4()
        self.instID = uuid.uuid4()
        self.proglang = "PYTHON"

        self.iDf = dataBundle()
        self.oDf = dataBundle()
        self.dispName = ""
        self.name = ""
        self.desc = ""
        self.tags = []

    @staticmethod
    def getRedOutputData(data):

        try:
            rData = redData(data.srvID, data.instID, data.sessionID)
            rData.data = data.oDf
            return rData

        except Exception as e:
            print(f"failed to sourceInfo getRedOutputData {e}")
            return None

    @staticmethod
    def toJsonString(src):
        str = ""
        try:
            str = json.dumps(src)

        except Exception as e:
            print(f"failed to sourceInfo toJsonString {e}")
            str = ""

        return str
