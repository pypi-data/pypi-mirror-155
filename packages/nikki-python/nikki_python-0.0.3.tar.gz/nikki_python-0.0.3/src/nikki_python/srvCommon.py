
import enum

class servCommMsgType(enum.Enum):
    srvData = "srvData",
    srvConnected = "srvConnected",
    srvNotMapped = "srvNotMapped",
    srvDisConnected = "srvDisConnected",
    removeSession = "removeSession",
    msgSent = "msgSent",
    pingResp = "pingResp",
    ok = "ok",
    error = "error",
    ping = "ping",
    dataSizeLimitExcess = "dataSizeLimitExcess",
    multipleDashboards = "multipleDashboards",
    dataConvertFailed = "dataConvertFailed",
    undefinedType = "undefinedType",
    maxConnection = "maxConnection",
    tooBigMsg = "tooBigMsg",
    msgRepeat = "msgRepeat",
    invalidSessionConnectTry = "invalidSessionConnectTry",
    inFlowMsgLimitExceed = "inFlowMsgLimitExceed"
    wsConnected = "wsConnected",
    wsTimeOut = "wsTimeOut",
    wsError = "wsError",
    wsDisconnected = "wsDisconnected",
    wsInvalidCred = "wsInvalidCred",
    wsInvalidSession = "wsInvalidSession",
    wsServiceNotStarted = "wsServiceNotStarted",
    wsServerDisconnected = "wsServerDisconnected"


class responseType(enum.Enum):
    ok = "ok",
    serverError = "serverError",
    invalidData = "invalidData",
    invalidRequest = "invalidRequest",
    insufficientPerm = "insufficientPerm",
    unknowError = "unknowError",
    dataNotFound = "dataNotFound",
    noConnection = "noConnection"


class validBasePath(enum.Enum):
    getServiceDataBySessionID = "/getServiceDataBySessionID"


class getServiceDataBySessionIDRequest():
    sessionID = ""
    srvUUId = ""


class wsMsgActionTypes(enum.Enum):
    srvMsg = "srvMsg"
  


class commonConst:
    serviceTokenFileName = "serviceToken.json"
    serviceDefFileName = "serviceDef.json"


class wsMsgWrapper:
    action = wsMsgActionTypes.srvMsg.value
    data = ""


class wsDataType:
    data = ""
    type = servCommMsgType.undefinedType.value


def wsMsgEncoder(msg):
    if isinstance(msg, wsMsgWrapper):
        return {}
    else:
        raise TypeError("failed to convert msg ")


class queryConst:
    runServiceKey = "runService"
    wsKey = "wsKey"
    sessionQueryKey = "sessionQueryKey"


class sessionTokenBase:
    name = ""
    version = 0.1
    sessionID = ""
    wsAddr = ""
    userID = ""

maxMsgLength = 350
pingTime = 26

class servMsgType(enum.Enum):
    service = "service",
    dash = "dash"