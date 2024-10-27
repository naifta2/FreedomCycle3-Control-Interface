// FreedomCycle3_Firmware.ino

// Define sensor pins
const int flowSensorPin1 = 21;
const int flowSensorPin2 = 22;
const int pressureSensorPin = A0; // Analog pin for pressure transducer

// Variables for sensor values
volatile int pulseCount1 = 0;
volatile int pulseCount2 = 0;
float flowRate1 = 0;
float flowRate2 = 0;
float pressureValue = 0;
unsigned long oldTime = 0;

// Valve control pin
const int valvePin = 13;

void setup() {
  Serial.begin(115200);

  // Initialize flow sensor pins
  pinMode(flowSensorPin1, INPUT_PULLUP);
  pinMode(flowSensorPin2, INPUT_PULLUP);

  // Initialize valve control pin
  pinMode(valvePin, OUTPUT);
  digitalWrite(valvePin, LOW); // Valve is initially closed

  // Attach interrupts for flow sensors
  attachInterrupt(digitalPinToInterrupt(flowSensorPin1), countPulses1, FALLING);
  attachInterrupt(digitalPinToInterrupt(flowSensorPin2), countPulses2, FALLING);
}

void loop() {
  // Calculate flow rate every second
  if (millis() - oldTime >= 1000) {
    // Disable interrupts during calculation
    detachInterrupt(digitalPinToInterrupt(flowSensorPin1));
    detachInterrupt(digitalPinToInterrupt(flowSensorPin2));

    // Calculate flow rates
    flowRate1 = (pulseCount1 / 7.5); // Adjust based on sensor specs
    flowRate2 = (pulseCount2 / 7.5);

    // Read pressure sensor
    pressureValue = analogRead(pressureSensorPin);
    pressureValue = map(pressureValue, 0, 1023, 0, 2000); // Adjust mapping based on sensor specs

    // Send data
    Serial.print("FLOW1:");
    Serial.print(flowRate1);
    Serial.print(",FLOW2:");
    Serial.print(flowRate2);
    Serial.print(",PRESSURE:");
    Serial.println(pressureValue);

    // Reset pulse counts and time
    pulseCount1 = 0;
    pulseCount2 = 0;
    oldTime = millis();

    // Re-attach interrupts
    attachInterrupt(digitalPinToInterrupt(flowSensorPin1), countPulses1, FALLING);
    attachInterrupt(digitalPinToInterrupt(flowSensorPin2), countPulses2, FALLING);
  }

  // Check for incoming commands
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    processCommand(command);
  }
}

void countPulses1() {
  pulseCount1++;
}

void countPulses2() {
  pulseCount2++;
}

void processCommand(String command) {
  if (command == "OPEN_VALVE") {
    digitalWrite(valvePin, HIGH);
  } else if (command == "CLOSE_VALVE") {
    digitalWrite(valvePin, LOW);
  }
}
