#include <Wire.h>
#include <Adafruit_PN532.h>
#define PN532_SCK  (5)
#define PN532_MOSI (3)
#define PN532_SS   (2)
#define PN532_MISO (4)

#define DEVICE_ID 1

Adafruit_PN532 nfc(PN532_SCK, PN532_MISO, PN532_MOSI, PN532_SS);

void setupNFC();
void nextUid();

void setup()
{
    Serial.begin(9600);
    setupNFC();
}

void loop()
{
    nextUid();
    delay(1500);
}

void setupNFC()
{
    nfc.begin();

    uint32_t version = nfc.getFirmwareVersion();
    Serial.flush();
    Serial.println();
    Serial.flush(); // ensure buffer is clear for writing
    if(!version)
    {
        Serial.println("{\"error\": \"Unable to find PN532\"}");
        while (1);
    }
    
    Serial.print("{\"model\": \"PN5"); Serial.print((version>>24) & 0xFF, HEX);
    Serial.print("\", \"firm\":\""); Serial.print((version>>16) & 0xFF, DEC);
    Serial.print('.'); Serial.print((version>>8) & 0xFF, DEC);
    Serial.println("\"}");
}

void nextUid()
{
    uint8_t uid[] = {0,0,0,0,0,0,0};
    uint8_t uidLength;
    
    boolean success;

    success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, &uid[0], &uidLength);

    if(!success)
    {
        return;
    }
    Serial.print("{\"device\":");
    Serial.print(DEVICE_ID);
    Serial.print(", \"uid\":\"");
    for(uint8_t i = 0; i < uidLength; i++)
    {
        Serial.print(uid[i], HEX);
    }
    Serial.println("\"}");
}
