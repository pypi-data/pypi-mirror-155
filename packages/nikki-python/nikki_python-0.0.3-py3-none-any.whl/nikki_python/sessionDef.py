

from src.sourceInfo import sourceInfo
from src.srvCommon import servMsgType

class serviceJoinInfo:
    sessionID =''
    userID = ""
    srv = sourceInfo()
    wsAddr = '' 
    type = servMsgType.service.value
