// FreedomCycle3_Firmware.ino

// Define sensor pins
const int flowSensorPin1 = 21;
const int flowSensorPin2 = 22;
const int pressureSensorPin1 = A0; // Analog pin for pressure transducer 1
const int pressureSensorPin2 = A1; // Analog pin for pressure transducer 2
const int pressureSensorPin3 = A2; // Analog pin for pressure transducer 3

// Variables for sensor values
volatile int pulseCount1 = 0;
volatile int pulseCount2 = 0;
float flowRate1 = 0;
float flowRate2 = 0;
float pressureValue1 = 0;
float pressureValue2 = 0;
float pressureValue3 = 0;
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

    // Read pressure sensors
    pressureValue1 = analogRead(pressureSensorPin1);
    pressureValue2 = analogRead(pressureSensorPin2);
    pressureValue3 = analogRead(pressureSensorPin3);

    // Convert analog readings to voltages
    float voltage1 = pressureValue1 * (5.0 / 1023.0);
    float voltage2 = pressureValue2 * (5.0 / 1023.0);
    float voltage3 = pressureValue3 * (5.0 / 1023.0);

    // Convert voltages to pressure values (0.5V to 4.5V corresponds to 0 to 200 psi)
    pressureValue1 = (voltage1 - 0.5) * (200.0 / 4.0);
    pressureValue2 = (voltage2 - 0.5) * (200.0 / 4.0);
    pressureValue3 = (voltage3 - 0.5) * (200.0 / 4.0);

    // Ensure pressure values are within range
    pressureValue1 = constrain(pressureValue1, 0, 200);
    pressureValue2 = constrain(pressureValue2, 0, 200);
    pressureValue3 = constrain(pressureValue3, 0, 200);

    // Send data
    Serial.print("FLOW1:");
    Serial.print(flowRate1);
    Serial.print(",FLOW2:");
    Serial.print(flowRate2);
    Serial.print(",PRESSURE1:");
    Serial.print(pressureValue1);
    Serial.print(",PRESSURE2:");
    Serial.print(pressureValue2);
    Serial.print(",PRESSURE3:");
    Serial.println(pressureValue3);

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
