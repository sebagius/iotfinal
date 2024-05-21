#define IIC_SCL A5
#define IIC_SDA A4
#define GREEN_LED1 2
#define GREEN_LED2 3
#define RED_LED1 5
#define RED_LED2 6
#include <ArduinoJson.h>


void setup()
{
   Serial.begin(9600);
  pinMode(IIC_SCL, OUTPUT);
  pinMode(IIC_SDA, OUTPUT);
  pinMode(GREEN_LED1, OUTPUT);
  pinMode(GREEN_LED2, OUTPUT);
  pinMode(RED_LED1, OUTPUT);
  pinMode(RED_LED2, OUTPUT);
  digitalWrite(IIC_SCL, LOW);
  digitalWrite(IIC_SDA, LOW);
  // Initially turn off all LEDs
  digitalWrite(GREEN_LED1, LOW);
  digitalWrite(GREEN_LED2, LOW);
  digitalWrite(RED_LED1, LOW);
  digitalWrite(RED_LED2, LOW);
  unsigned char table[16] = {0x00, 0x32, 0x2A, 0x26, 0x00, 0x32, 0x2A, 0x26, 0x00, 0x3E, 0x00, 0x16, 0x28, 0x28, 0x3E, 0x00};
  updateDisplay(table);
}


void loop()
{
  String msg = Serial.readStringUntil('\n');
  msg.trim();
  if(msg.length() ==0)
    return;
  delay(5);
  StaticJsonDocument<200> doc;

  DeserializationError error = deserializeJson(doc, msg.c_str());


if (error) {
  Serial.print(F("deserializeJson() failed: "));
  Serial.println(error.f_str());
  return;
}
const char* id=doc["uid"];
int device = doc["device"];
int allowed = doc["allow"];
  digitalWrite(GREEN_LED1, (device == 1 && allowed == 1) ? HIGH : LOW);
  digitalWrite(GREEN_LED2, (device == 2 && allowed == 1) ? HIGH : LOW);
  digitalWrite(RED_LED1, (device == 1 && allowed == 0) ? HIGH : LOW);
  digitalWrite(RED_LED2, (device == 2 && allowed == 0) ? HIGH : LOW);
String uid = String(id);

unsigned char table[16] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
int j= 0;
for(int i = 0; i < uid.length(); i += 2) {
  String hexPair = uid.substring(i, i+2);
  table[j] = (unsigned char) strtoul(hexPair.c_str(), NULL, 16);
  j++;
}
updateDisplay(table);
}  
/* Code below this point is based on the datasheet for the LCD Matrix - modified by myself */

void updateDisplay(unsigned char tb[16])
{
  IIC_start();
  IIC_send(0x40);
  IIC_end();
  IIC_start();
  IIC_send(0xc0);// set the initial address as 0

  /* Data Display */
  for (char i = 0; i < 16; i++)
  {
    IIC_send(tb[i]);
  }
  IIC_end();

 
  /* brightness */
  IIC_start();
  IIC_send(0x8A);
  IIC_end();
}

/* Code below here is directly taken from the LCD Matrix datasheet without modification */
/* Couldn't get hardware i2c working so had to rely on software i2c instead */
void IIC_start()
{
  digitalWrite(IIC_SCL, LOW);
  delayMicroseconds(3);
  digitalWrite(IIC_SDA, HIGH);
  delayMicroseconds(3);
  digitalWrite(IIC_SCL, HIGH);
  delayMicroseconds(3);
  digitalWrite(IIC_SDA, LOW);
  delayMicroseconds(3);
}

void IIC_send(unsigned char send_data)
{
  for (char i = 0; i < 8; i++)
  {
    digitalWrite(IIC_SCL, LOW);
    delayMicroseconds(3);
    if (send_data & 0x01)
    {
      digitalWrite(IIC_SDA, HIGH);
    }
    else
    {
      digitalWrite(IIC_SDA, LOW);
    }
    delayMicroseconds(3);
    digitalWrite(IIC_SCL, HIGH);
    delayMicroseconds(3);
    send_data = send_data >> 1;
  }
}

void IIC_end()
{
  digitalWrite(IIC_SCL, LOW);
  delayMicroseconds(3);
  digitalWrite(IIC_SDA, LOW);
  delayMicroseconds(3);
  digitalWrite(IIC_SCL, HIGH);
  delayMicroseconds(3);
  digitalWrite(IIC_SDA, HIGH);
  delayMicroseconds(3);
}