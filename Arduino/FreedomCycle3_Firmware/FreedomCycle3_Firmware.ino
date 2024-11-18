// FreedomCycle3_Firmware.ino

// Data Sample Rate
const int sampleRate = 100; // in milliseconds

// Valve open time in autonomous mode
const int autoModeValveTime = 500; // in milliseconds

const int flowSensorPin1 = 21;
const int pressureSensorPin1 = A0; 
const int pressureSensorPin2 = A1; 
const int pressureSensorPin3 = A2;
const int valvePin = 50;

volatile int pulseCount1 = 0;
int valveOpenTime= 0;
int valveWaitTime= 0;
float cumulativeFlow = 0;
float pressureValue1 = 0, pressureValue2 = 0, pressureValue3 = 0;
unsigned long oldTime = 0;
bool ValveState = false;
bool autonomousMode = false;
bool isValveTemporarilyOpen = false;

//PCB LED PINS
const int LED1 = 22;
const int LED2 = 23;
const int LED3 = 24;
const int LED4 = 25;
const int LED5 = 26;

// Bluetooth Module STATE Pin
const int Bluetooth = 27;

void setup() {
  Serial.begin(115200);  
  Serial1.begin(9600);

  // PCB LED setup
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);
  pinMode(LED4, OUTPUT);
  pinMode(LED5, OUTPUT);

  // Bluetooth module STATE pin setup.
  pinMode(Bluetooth, INPUT);

  // Set LED1 as Arduino STATE LED (on/off)
  digitalWrite(LED1, HIGH);

  pinMode(flowSensorPin1, INPUT_PULLUP);
  pinMode(valvePin, OUTPUT);
  digitalWrite(valvePin, LOW);
  digitalWrite(LED5, LOW);
  ValveState = false;

  attachInterrupt(digitalPinToInterrupt(flowSensorPin1), countPulses1, FALLING);
}

void loop() {
  if (millis() - oldTime >= sampleRate) {
    detachInterrupt(digitalPinToInterrupt(flowSensorPin1));
    cumulativeFlow += pulseCount1 / 596.0;
    pressureValue1 = convertToPSI(analogRead(pressureSensorPin1));
    pressureValue2 = convertToPSI(analogRead(pressureSensorPin2));
    pressureValue3 = convertToPSI(analogRead(pressureSensorPin3));

    sendData(Serial);
    sendData(Serial1);

    pulseCount1 = 0;
    oldTime = millis();
    attachInterrupt(digitalPinToInterrupt(flowSensorPin1), countPulses1, FALLING);
  }

  if(autonomousMode){
    digitalWrite(LED2, HIGH);
  }
  else if (!autonomousMode){
    digitalWrite(LED2, LOW);
  }
  // && millis() - valveWaitTime 
  if (autonomousMode && pressureValue2 <= 0.1 && cumulativeFlowStable() && millis() - valveWaitTime >= 5000) {
    openValveTemporarily();
  }

  if (isValveTemporarilyOpen && millis() - valveOpenTime >= autoModeValveTime) {
    valveWaitTime = millis();
    closeValve();
  }

  checkCommands(Serial);
  checkCommands(Serial1);
}

float convertToPSI(int analogValue) {
  float voltage = analogValue * (5.0 / 1023.0);
  return constrain((voltage - 0.5) * (200.0 / 4.0), 0, 200);
}

void sendData(HardwareSerial &serialPort) {
  serialPort.print("PROGRAM:");
  serialPort.print(true);
  serialPort.print(",AUTO_MODE:");
  serialPort.print(autonomousMode);
  serialPort.print(",CUMULATIVE_FLOW:");
  serialPort.print(cumulativeFlow);
  serialPort.print(",PRESSURE1:");
  serialPort.print(pressureValue1);
  serialPort.print(",PRESSURE2:");
  serialPort.print(pressureValue2);
  // serialPort.print(",PRESSURE3:");
  // serialPort.print(pressureValue3);
  serialPort.print(",VALVE_STATE:");
  serialPort.println(ValveState);
}

bool cumulativeFlowStable() {
  static float lastFlow = 0;
  static unsigned long lastStableTime = millis();
  if (abs(cumulativeFlow - lastFlow) < 0.01) {
    if (millis() - lastStableTime > 500) {
      return true;
    }
  } else {
    lastStableTime = millis();
  }
  lastFlow = cumulativeFlow;
  return false;
}

void openValveTemporarily() {
  digitalWrite(valvePin, HIGH);
  digitalWrite(LED5, HIGH);
  ValveState = true;
  valveOpenTime = millis();
  isValveTemporarilyOpen = true;
}

void closeValve() {
  digitalWrite(valvePin, LOW);
  digitalWrite(LED5, LOW);
  ValveState = false;
  isValveTemporarilyOpen = false;
}

void openValve(){
  digitalWrite(valvePin, HIGH);
  digitalWrite(LED5, HIGH);
  ValveState = true;
}

void checkCommands(HardwareSerial &serialPort) {
  if (serialPort.available() > 0) {
    String command = serialPort.readStringUntil('\n');
    processCommand(command);
  }
}

void countPulses1() {
  pulseCount1++;
}

void processCommand(String command) {
  if (command == "OPEN_VALVE") {
    openValve();
  } else if (command == "CLOSE_VALVE") {
    closeValve();
  } else if (command == "RESET_CUMULATIVE_FLOW") {
    cumulativeFlow = 0.0;
  } else if (command == "ENABLE_AUTO") {
    autonomousMode = true;
    digitalWrite(LED2, HIGH);
  } else if (command == "DISABLE_AUTO") {
    autonomousMode = false;
    digitalWrite(LED2, LOW);
  }
}
