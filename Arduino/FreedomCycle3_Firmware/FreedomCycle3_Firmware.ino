// FreedomCycle3_Firmware.ino

const int flowSensorPin1 = 21;
const int pressureSensorPin1 = A0; 
const int pressureSensorPin2 = A1; 
const int pressureSensorPin3 = A2;
const int valvePin = 50;

volatile int pulseCount1 = 0;
int valveOpenTime= 0;
float cumulativeFlow = 0;
float pressureValue1 = 0, pressureValue2 = 0, pressureValue3 = 0;
unsigned long oldTime = 0;
bool ValveState = false;
bool autonomousMode = false;
bool isValveTemporarilyOpen = false;

void setup() {
  Serial.begin(115200);  
  Serial1.begin(9600);  

  pinMode(flowSensorPin1, INPUT_PULLUP);
  pinMode(valvePin, OUTPUT);
  digitalWrite(valvePin, LOW);
  ValveState = false;

  attachInterrupt(digitalPinToInterrupt(flowSensorPin1), countPulses1, FALLING);
}

void loop() {
  if (millis() - oldTime >= 1000) {
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

  if (autonomousMode && pressureValue2 == 0 && cumulativeFlowStable()) {
    openValveTemporarily();
  }

  if (isValveTemporarilyOpen && millis() - valveOpenTime >= 500) {
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
  serialPort.print(",PRESSURE3:");
  serialPort.print(pressureValue3);
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
  ValveState = 1;
  valveOpenTime = millis();
  isValveTemporarilyOpen = true;
}

void closeValve() {
  digitalWrite(valvePin, LOW);
  ValveState = 0;
  isValveTemporarilyOpen = false;
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
    digitalWrite(valvePin, HIGH);
    ValveState = true;
  } else if (command == "CLOSE_VALVE") {
    digitalWrite(valvePin, LOW);
    ValveState = false;
  } else if (command == "RESET_CUMULATIVE_FLOW") {
    cumulativeFlow = 0.0;
  } else if (command == "ENABLE_AUTO") {
    autonomousMode = true;
  } else if (command == "DISABLE_AUTO") {
    autonomousMode = false;
  }
}
