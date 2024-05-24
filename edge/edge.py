from device import NFCDevice, LEDDevice
import threading
from edge_db import EdgeDatabase

def nfc_loop(dev, num, led):
    while True:
        m = dev.nextMessage()
        if not m:
            continue
        if 'uid' in m:
            led.sendMessage(m)

def main():
    db = EdgeDatabase('localhost', 5432)
    leddev = LEDDevice('/dev/ttyACM0')
    nfcdev_1 = NFCDevice('/dev/ttyACM1', "NWGo6NhgDisVXSc9nv1C", db, 1)
    nfcdev_2 = NFCDevice('/dev/ttyACM2', "M69d8qPEbQmEjqyhhN5h", db, 2)
    
    x1 = threading.Thread(target=nfc_loop, args=(nfcdev_1, 1, leddev))
    x2 = threading.Thread(target=nfc_loop, args=(nfcdev_2, 2, leddev))
    x1.start()
    x2.start()
    while True:
        pass
    

if __name__ == "__main__":
    main()
