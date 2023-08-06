from sessionDef import serviceJoinInfo
from srvCommon import queryConst, servMsgType

import json
import base64


class wsAddress:
    @staticmethod
    def getWsAddress(servDef, token):

        wsAddrs = None
        try:
            wsTokenExch = serviceJoinInfo()
            wsTokenExch.sessionID = token["sessionID"]
            wsTokenExch.userID = token["userID"]
            wsTokenExch.type = servMsgType.service.name
            wsTokenExch.srv = servDef

            strToken = json.dumps(wsTokenExch.__dict__)

            message_bytes = strToken.encode('ascii')
            # print("encode = > ", message_bytes)
            base64_bytes = base64.b64encode(message_bytes)
            # print("base64_bytes = > ", base64_bytes)
            base64_message = base64_bytes.decode('ascii')

            strQuery = f"?{queryConst.wsKey}={base64_message}"

            wsBase = token["wsAddr"]
            wsAddrs = f"{wsBase}{strQuery}"

           
        except Exception as e:
            print("exception : wsAddress getWsAddress() ", e)
            wsAddrs = None
            
        return wsAddrs
