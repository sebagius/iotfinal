import serial
import json
import requests

approvedCard = "222CB834" # this would come from a database but for simplicity we are hardcoding

class Device:
    def __init__(self, port):
        self._ser = serial.Serial(port, 9600)
    
    def nextMessage(self):
        msg = self._ser.readline()
        msg = msg.decode('utf-8').strip()
        if not msg:
            return None
        return json.loads(msg)

    def sendMessage(self, msg):
        m = json.dumps(msg)
        self._ser.write(m.encode('utf-8'))
        self._ser.write(b"\n")

class NFCDevice(Device):

    def __init__(self, port, url):
        super().__init__(port)
        self._url = url

    def nextMessage(self):
        x = super().nextMessage()
        if x is None:
            return None
        if 'uid' in x:
            if x['uid'] == approvedCard:
                x['allow'] = 1
            else:
                x['allow'] = 0
            requests.post(self._url, json=x)
        return x

class LEDDevice(Device):
    pass
