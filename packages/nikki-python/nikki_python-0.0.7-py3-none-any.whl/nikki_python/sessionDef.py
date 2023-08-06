

from nikki_python.sourceInfo import sourceInfo
from nikki_python.srvCommon import servMsgType

class serviceJoinInfo:
    sessionID =''
    userID = ""
    srv = sourceInfo()
    wsAddr = '' 
    type = servMsgType.service.value
