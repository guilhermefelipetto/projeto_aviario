#include <DHT11.h> 
#include <SPI.h>

#include <MFRC522.h>

#include <HX711_ADC.h>
#if defined(ESP8266)|| defined(ESP32) || defined(AVR)
#include <EEPROM.h>
#endif

#include <BH1750.h>
#include <Wire.h>

BH1750 lightMeter;

// Create an instance of the DHT11 class and set the digital I/O pin.
DHT11 dht11(2);

#define RST_PIN         9          // Configurável, veja o layout típico dos pinos acima
#define SS_PIN          10

byte readCard[4];
String MasterTag = "63D42E8C";
String tagID = "";

MFRC522 mfrc522(SS_PIN, RST_PIN);

//pins:
const int HX711_dout = 4; //mcu > HX711 dout pin
const int HX711_sck = 5; //mcu > HX711 sck pin

//HX711 constructor:
HX711_ADC LoadCell(HX711_dout, HX711_sck);

const int calVal_eepromAdress = 0;
unsigned long t = 0;

void setup()
{
    // Inicia a comunicação serial com o console de todos os módulos (9600)
    Serial.begin(9600);		
    SPI.begin();			// Inicia o barramento SPI
    mfrc522.PCD_Init();		//Inicia o  MFRC522
    delay(10);				// Atraso opcional. Algumas placas precisam de mais tempo após o init para ficarem prontas, veja Readme
    mfrc522.PCD_DumpVersionToSerial();	// Mostrar detalhes do leitor de cartão PCD - MFRC522
    Serial.println("--------------------------");
    Serial.println("Controle de Acesso");
    Serial.println("Aproxime o Cartão");
    Serial.println();
    Serial.println("Iniciando Pesagem...");
    Wire.begin();
    LoadCell.begin();
    lightMeter.begin();
    Serial.println(F("BH1750 Test begin"));

    //LoadCell.setReverseOutput(); //uncomment to turn a negative output value to positive
    float calibrationValue; // calibration value (see example file "Calibration.ino")
    calibrationValue = 696.0; // uncomment this if you want to set the calibration value in the sketch
    #if defined(ESP8266)|| defined(ESP32)
    EEPROM.begin(512); // uncomment this if you use ESP8266/ESP32 and want to fetch the calibration value from eeprom
    #endif
    EEPROM.get(calVal_eepromAdress, calibrationValue); // uncomment this if you want to fetch the calibration value from eeprom

    unsigned long stabilizingtime = 2000; // preciscion right after power-up can be improved by adding a few seconds of stabilizing time
    boolean _tare = true; //set this to false if you don't want tare to be performed in the next step
    LoadCell.start(stabilizingtime, _tare);
    if (LoadCell.getTareTimeoutFlag()) {
      Serial.println("Timeout, check MCU>HX711 wiring and pin designations");
      while (1);
    }
    else {
      LoadCell.setCalFactor(calibrationValue); // set calibration value (float)
      Serial.println("Startup is complete");
    }
         
      
}

void loop()
{
    // Read the humidity from the sensor.
    float humidity = dht11.readHumidity(); //GUILHERME CONECTAR SE A ESTA VARIAVEL PARA UMIDADE

    // Read the temperature from the sensor.
    float temperature = dht11.readTemperature(); //GUILHERME CONECTAR SE A ESTA VARIAVEL PARA TEMPERATURA

    // If the temperature and humidity readings were successful, print them to the serial monitor.
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
        // If the temperature or humidity reading failed, print an error message.
        Serial.println("Error reading data");
    }

    // Wait for 2 seconds before the next reading.
    delay(2000);
    
    
      //----------------------------------------------------------------------
  //----------------------------------------------------------------------
  //Wait until new tag is available
  while (getID()) {
    //MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
    if (tagID == MasterTag){
      Serial.println(" Access Granted!");
      Serial.println("--------------------------");
       //You can write any code here like, opening doors, 
       //switching ON a relay, lighting up an LED etc...
    }
    //MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
    else{
      Serial.println(" Access Denied!");
      Serial.println("--------------------------");
    }
    //MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
    delay(2000);
    Serial.println(" Access Control ");
    Serial.println("Scan Your Card>>");
  }
  //----------------------------------------------------------------------
  static boolean newDataReady = 0;
  const int serialPrintInterval = 0; //increase value to slow down serial print activity

  // check for new data/start next conversion:
  if (LoadCell.update()) newDataReady = true;

  // get smoothed value from the dataset:
  if (newDataReady) {
    if (millis() > t + serialPrintInterval) {
      float i = LoadCell.getData();
      Serial.print("Load_cell output val: ");
      Serial.println(i);
      newDataReady = 0;
      t = millis();
    }
  }

  // receive command from serial terminal, send 't' to initiate tare operation:
  if (Serial.available() > 0) {
    char inByte = Serial.read();
    if (inByte == 't') LoadCell.tareNoDelay();
  }

  // check if last tare operation is complete:
  if (LoadCell.getTareStatus() == true) {
    Serial.println("Tare complete");
  }

    float lux = lightMeter.readLightLevel();
    Serial.print("Light: ");
    Serial.print(lux);
    if (lux > 100)
    {
      // ação desejada
    }  
    Serial.println(" lx");
    delay(1000);

}




/**********************************************************************************************
 * getID() function
 * Read new tag if available
**********************************************************************************************/
boolean getID() 
{
  //MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
  // Getting ready for Reading PICCs
  //If a new PICC placed to RFID reader continue
  if ( ! mfrc522.PICC_IsNewCardPresent()) {
    return false;
  }
  //MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
  //Since a PICC placed get Serial and continue
  if ( ! mfrc522.PICC_ReadCardSerial()) {
  return false;
  }
  //MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
  tagID = "";
  // The MIFARE PICCs that we use have 4 byte UID
  for ( uint8_t i = 0; i < 4; i++) {
  //readCard[i] = mfrc522.uid.uidByte[i];
  // Adds the 4 bytes in a single String variable
  tagID.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  //MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
  tagID.toUpperCase();
  mfrc522.PICC_HaltA(); // Stop reading
  return true;
  //MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
}
