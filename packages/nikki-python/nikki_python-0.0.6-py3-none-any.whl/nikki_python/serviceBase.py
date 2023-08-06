from json import encoder
import sys
import threading
import json
import time
from nikki_python.addressUtil import wsAddress
from nikki_python.configHandler import configHandler
from nikki_python.encoders import pySourceInfoEncoder
from nikki_python.redData import redData
from nikki_python.sourceInfo import sourceInfo
from nikki_python.srvCommon import servCommMsgType, maxMsgLength, pingTime

import websocket


class servieBase:
    _wsInst = None
    _isConnectedFlag = False
    _startedFlag = False
    _token = None
    _mainThreadInst = None
    _pingThreadInst = None

    def __init__(self):
        self._srvInfo = sourceInfo()

    def _wsOnConnect(self, ws):
        self._isConnectedFlag = True
        try:
            self.onConnected()
        except Exception as e:
            print("exception while onConnect msg handling. " + str(e))

    def _wsOnDisconnect(self, ws, close_status):

        self._isConnectedFlag = False
        try:
            self.onDisconnected()
        except Exception as e:
            print("exception while onDisconnect msg handling. " + str(e))

    def _wsOnError(self, ws, msg):
        self._isConnectedFlag = False
        print("ERROR : " + str(msg))
        try:
            self.onError(msg)
        except Exception as e:
            print("exception while onError msg handling. " + str(e))

    def onConnected(self):
        print("connected.")
        pass

    def onDisconnected(self):
        print("dis-connected.")
        pass

    def onError(self, msg):
        print("error: ", msg)
        pass

    def onData(self, data):
        print("received data ", data)
        pass

    def _onWsInputMsg(self, ws, msg):
        try:
            # print("got  msg ", msg)

            inMsg = json.loads(msg)

            if (('data' in inMsg) and ('data' in inMsg['data'])):
                try:
                    # print("this is inside", inMsg['data']['data'])
                    self.onData(inMsg['data']['data'])
                except Exception as e:
                    print("failed to handling input msg ", e)
            # else:
                # print("invalid node msg ", msg)

        except Exception as e:
            print("failed to process input msg ", msg, e)

    def _startPing(self):
        try:
            while (self._startedFlag == True):
                time.sleep(pingTime)
                if(self._isConnectedFlag == True):

                    pingMsg = {}
                    pingMsg['action'] = servCommMsgType.ping.name
                    pingMsg['sessionID'] = self._token['sessionID']

                    strMsg = json.dumps(pingMsg)

                    # print('pingMsg..... ')
                    self._wsInst.send(strMsg)

        except Exception as e:
            print("exception while ping  " + str(e))

    def start(self):
        try:
            print("getting service information.")
            self._srvInfo = configHandler.getServiceDef()
            self._token = configHandler.getTokenDef()
            wsAddr = wsAddress.getWsAddress(self._srvInfo, self._token)

            if((wsAddr != None) and (len(wsAddr) > 0) and (self._startedFlag == False)):

                try:

                    print("connecting to server...")
                    self._wsInst = websocket.WebSocketApp(wsAddr,
                                                          on_open=self._wsOnConnect,
                                                          on_message=self._onWsInputMsg,
                                                          on_error=self._wsOnError,
                                                          on_close=self._wsOnDisconnect)

                    self._mainThreadInst = threading.Thread(
                        target=self._wsInst.run_forever)

                    self._pingThreadInst = threading.Thread(
                        target=self._startPing)

                    self._mainThreadInst.daemon = True
                    self._mainThreadInst.start()
                    self._pingThreadInst.start()
                    self._startedFlag = True

                except Exception as e:
                    print("exception : while starting:  ", e)

            else:
                print("invalide address received, check sessionToken.json and sericeDef.json files ", wsAddr)

        except Exception as e:
            print("failed to start pyServieBase start()", e)

    def stop(self):
        print("stopping service")
        try:
            self._isConnectedFlag = False
            if (self._wsInst is not None) and (self._wsInst.close is not None):

                self._wsInst.close()

                self._mainThreadInst.join(timeout=1)
                self._pingThreadInst.join(timeout=1)

                print("stopped service.")
                sys.exit()

        except Exception as e:
            print("failed to stop ", e)

    def sendData(self, data):
        try:

            if((self._isConnectedFlag == True) and (self._startedFlag == True)):
                dataValid = self._isInputDataValid(data)
                if((dataValid != None)):
                    self._wsInst.send(dataValid)
        except Exception as e:
            print("exception while sending data " + str(e))

    def _isInputDataValid(self, data):
        stat = None
        try:

            outMsg = self._getOutRedData()
            # print('======+++++++=> outMsg msg ',
            #       outMsg["data"], outMsg["data"]["data"])
            outMsg["data"]["data"] = data

            tobj = pySourceInfoEncoder(outMsg)
            # print('----------####################>encodeedd ',
            #       tobj)
            strMsg = json.dumps(tobj)
            # print('####################>reassigned ',
            #       tobj)
            # print('sending msg ', strMsg, type(str(strMsg)), type(strMsg.__repr__()))
            # cleanStr = strMsg.replace("resp","")

            msgLen = len(strMsg)
            if(msgLen > maxMsgLength):
                stat = None
                print(str(servCommMsgType.dataSizeLimitExcess))

            else:
                stat = strMsg

        except Exception as e:
            print("failed to process input msg ",  e)
            stat = None
        return stat

    def _getInputBundle(self):
        return self._srvInfo.iDf

    def _getOutputBundle(self):
        return self._srvInfo.oDf

    def _toJsonString(self):
        str = ""
        try:
            str = json.dumps(self._srvInfo)
        except Exception as e:
            print(f"failed to convert json object as string {e}")
            str = ""
        return str

    def _getOutRedData(self):
        # print("------------------------------>", self.srvInfo["srvUUId"],
        #       self.srvInfo["srvClientID"],
        #       self.srvInfo["srvInstID"])
        srvData = redData(self._srvInfo["srvID"],
                          self._srvInfo["instID"],
                          self._token["sessionID"])

        srvData.data = self._srvInfo["oDf"]
        # print("srv ====================!!!!!!!!!!!!! ",
        #   srvData, srvData["redData"])
        # print("type ", type(srvData))
        # print("type =>  ", dict(srvData.__dict__))
        return srvData.__dict__
        # if (self.srvInfo != None):

        #     srvData = redData(self.srvInfo["srvUUId"],
        #                     self.srvInfo["srvClientID"], self.srvInfo["srvInstID"])
        #     srvData.data = self.srvInfo["oDf"]
        #     print("srv ====================!!!!!!!!!!!!! ",srvData, srvData["redData"])
        #     return srvData
        # else:
        #     return None


# def encode():
#     if isinstance(perm ,):

#     raise TypeError('servi')
