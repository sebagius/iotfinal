import serial
import json
import requests
import paho.mqtt.client as mqtt

approvedCard = "41B1C72A86180" # this would come from a database but for simplicity we are hardcoding

class Device:
    def __init__(self, port, idi=None):
        self._ser = serial.Serial(port, 9600)
        self._idi = idi
    
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

    def __init__(self, port, access, db, idi=None):
        super().__init__(port, idi)
        self._acc = access
        self.client = mqtt.Client()
        self.client.username_pw_set(self._acc)
        self.client.connect('thingsboard.cloud', 1883, 60)
        self.client.loop_start()
        self.db = db

    def nextMessage(self):
        x = super().nextMessage()
        if x is None:
            return None
        if 'uid' in x:
            if x['uid'] == approvedCard:
                x['allow'] = 1
            else:
                x['allow'] = 0
            self.db.log(x['uid'], self._idi) 
            print("[Received ID] {}".format(x['uid']))
            try:
                self.client.publish('v1/devices/me/telemetry', json.dumps(x))
            except:
                print("Cloud Connection Failed...")
        return x

class LEDDevice(Device):
    pass
