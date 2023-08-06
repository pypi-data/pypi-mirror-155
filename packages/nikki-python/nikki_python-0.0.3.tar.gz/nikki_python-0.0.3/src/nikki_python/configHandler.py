import os
import json

from src.srvCommon import commonConst


class configHandler:
    @staticmethod
    def getServiceDef():
        srvDef = ""
        fPath = configHandler.getServiceDefPath()
        with open(fPath) as fh:
            try:
                srvDef = json.load(fh)
                # print(f"service def {srvDef}")
            except Exception as e:
                print(e)
        return srvDef

    @staticmethod
    def getTokenDef():
        token = ""
        fPath = configHandler.getServiceTokenPath()
        with open(fPath) as fh:
            try:
                token = json.load(fh)
                # print(f"token def {token}")
            except Exception as e:
                print(e)
        return token

    @staticmethod
    def getServiceDefPath():
        spath = os.path.join(os.getcwd(
        ),  commonConst.serviceDefFileName)
        return spath

    @staticmethod
    def getServiceTokenPath():
        spath = os.path.join(os.getcwd(
        ), commonConst.serviceTokenFileName)
        return spath
