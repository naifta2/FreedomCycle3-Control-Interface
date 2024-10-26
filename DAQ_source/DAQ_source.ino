// Define sensor input pin
const int flowSensorPin = 21;

// Variables to store pulse count and flow rate
volatile int pulseCount = 0;
float flowRate = 0;
unsigned long oldTime = 0;

void setup() {
  // Initialize serial communication for debugging
  Serial.begin(9600);

  // Set the pin as input
  pinMode(flowSensorPin, INPUT_PULLUP);

  // Attach an interrupt to the pin, triggering on the falling edge
  attachInterrupt(digitalPinToInterrupt(flowSensorPin), countPulses, FALLING);
}

void loop() {
  // Calculate flow rate once per second (1000ms)
  if (millis() - oldTime >= 500) {
    // Calculate flow rate (L/min)
    flowRate = (pulseCount / 3.75);  // 7.5 pulses per second per L/min for this sensor

    // Print flow rate in L/min
    Serial.print(flowRate, "\n");

    // Reset pulse count and update time
    pulseCount = 0;
    oldTime = millis();
  }
}

// Interrupt function to count pulses
void countPulses() {
  pulseCount++;
}