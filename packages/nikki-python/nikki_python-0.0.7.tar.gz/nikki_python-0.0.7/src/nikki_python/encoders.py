
from nikki_python.srvCommon import servMsgType, wsMsgActionTypes


def pySourceInfoEncoder(pys):
    # if isinstance(pys, redData.redData):
    try:
        pRedy = {
            "action": wsMsgActionTypes.srvMsg.name,
            "sessionID": pys["sessionID"],
            "msg": pys["msg"],
            "srvID": pys["srvID"],
            "instID": pys["instID"],
            "data": {
                "name": pys["data"]["name"],
                "data": pys["data"]["data"],
                "desc": pys["data"]["desc"]
            },
            "status": pys["status"]
        }
        # print("json ", pRedy)
        return pRedy
    except Exception as e:
        print("failed to return obj ", e)
        return {}

    # return {
    #     "srvUUId": pys.srvUUId,
    #     "srvInstID": pys.srvInstID,
    #     "srvClientID": pys.srvClientID,
    #     "srvName": pys.srvName,
    #     "desc": pys.desc,
    #     "tags": pys.tags,

    # }
    # else:
    #     raise TypeError(f'failed to serialize sourceInfo')
#
