#include <DHT11.h>
#include <SPI.h>

#include <MFRC522.h>

#include <HX711_ADC.h>
#if defined(ESP8266) || defined(ESP32) || defined(AVR)
#include <EEPROM.h>
#endif

#include <BH1750.h>
#include <Wire.h>

BH1750 lightMeter;

DHT11 dht11(2);

#define RST_PIN 9
#define SS_PIN 10

byte readCard[4];
String MasterTag = "63D42E8C";
String tagID = "";

MFRC522 mfrc522(SS_PIN, RST_PIN);

const int HX711_dout = 4;
const int HX711_sck = 5;

HX711_ADC LoadCell(HX711_dout, HX711_sck);

const int calVal_eepromAdress = 0;
unsigned long t = 0;

void setup()
{
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  delay(10);
  mfrc522.PCD_DumpVersionToSerial();
  Serial.println("--------------------------");
  Serial.println("Controle de Acesso");
  Serial.println("Aproxime o Cartão");
  Serial.println();
  Serial.println("Iniciando Pesagem...");
  Wire.begin();
  LoadCell.begin();
  lightMeter.begin();
  Serial.println(F("BH1750 Test begin"));

  float calibrationValue;
  calibrationValue = 696.0;
#if defined(ESP8266) || defined(ESP32)
  EEPROM.begin(512);
#endif
  EEPROM.get(calVal_eepromAdress, calibrationValue);

  unsigned long stabilizingtime = 2000;
  boolean _tare = true;
  LoadCell.start(stabilizingtime, _tare);
  if (LoadCell.getTareTimeoutFlag())
  {
    Serial.println("Timeout, check MCU>HX711 wiring and pin designations");
    while (1)
      ;
  }
  else
  {
    LoadCell.setCalFactor(calibrationValue);
    Serial.println("Startup is complete");
  }
}

void loop()
{
  float humidity = dht11.readHumidity();

  float temperature = dht11.readTemperature();

  if (temperature != -1 && humidity != -1)
  {
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.println(" C");

    Serial.print("Humidity: ");
    Serial.print(humidity);
    Serial.println(" %");
  }
  else
  {
    Serial.println("Error reading data");
  }

  delay(2000);

  while (getID())
  {
    if (tagID == MasterTag)
    {
      Serial.println(" Access Granted!");
      Serial.println("--------------------------");
    }
    else
    {
      Serial.println(" Access Denied!");
      Serial.println("--------------------------");
    }
    delay(2000);
    Serial.println(" Access Control ");
    Serial.println("Scan Your Card>>");
  }
  static boolean newDataReady = 0;
  const int serialPrintInterval = 0;

  if (LoadCell.update())
    newDataReady = true;

  if (newDataReady)
  {
    if (millis() > t + serialPrintInterval)
    {
      float i = LoadCell.getData();
      Serial.print("Load_cell output val: ");
      Serial.println(i);
      newDataReady = 0;
      t = millis();
    }
  }

  if (Serial.available() > 0)
  {
    char inByte = Serial.read();
    if (inByte == 't')
      LoadCell.tareNoDelay();
  }

  if (LoadCell.getTareStatus() == true)
  {
    Serial.println("Tare complete");
  }

  float lux = lightMeter.readLightLevel();
  Serial.print("Light: ");
  Serial.print(lux);
  Serial.println(" lx");
  delay(1000);
}

boolean getID()
{
  if (!mfrc522.PICC_IsNewCardPresent())
  {
    return false;
  }
  if (!mfrc522.PICC_ReadCardSerial())
  {
    return false;
  }
  tagID = "";
  for (uint8_t i = 0; i < 4; i++)
  {
    tagID.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  tagID.toUpperCase();
  mfrc522.PICC_HaltA();
  return true;
}
