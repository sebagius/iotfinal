from device import NFCDevice, LEDDevice
import threading

def nfc_loop(dev, num, led):
    while True:
        m = dev.nextMessage()
        if not m:
            continue
        if 'uid' in m:
            led.sendMessage(m)

def main():
    leddev = LEDDevice('/dev/ttyACM0')
    nfcdev_1 = NFCDevice('/dev/ttyACM1', "http://thingsboard.cloud/api/v1/NWGo6NhgDisVXSc9nv1C/telemetry")
    nfcdev_2 = NFCDevice('/dev/ttyACM2', "http://thingsboard.cloud/api/v1/M69d8qPEbQmEjqyhhN5h/telemetry")
    
    x1 = threading.Thread(target=nfc_loop, args=(nfcdev_1, 1, leddev))
    x2 = threading.Thread(target=nfc_loop, args=(nfcdev_2, 2, leddev))
    x1.start()
    x2.start()
    while True:
        pass
    

if __name__ == "__main__":
    main()
