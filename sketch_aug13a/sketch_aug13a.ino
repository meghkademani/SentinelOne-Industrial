// SentinelOne Industrial
// MQ-2 / MQ-135 + HC-SR04

// Gas sensor
const int gasSensorPin = A0;

// HC-SR04
const int trigPin = 9;
const int echoPin = 10;

void setup() {
  Serial.begin(9600);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  Serial.println("================================");
  Serial.println("   SENTINELONE INDUSTRIAL");
  Serial.println("   Sensor Monitoring Started");
  Serial.println("================================");
}

void loop() {

  // -------------------------
  // Read Gas Sensor
  // -------------------------
  int gasValue = analogRead(gasSensorPin);

  // -------------------------
  // Read HC-SR04
  // -------------------------
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);

  digitalWrite(trigPin, LOW);

  // Wait for echo with timeout
  long duration = pulseIn(echoPin, HIGH, 30000);

  float distance;

  if (duration == 0) {
    distance = -1;
  } else {
    distance = duration * 0.0343 / 2;
  }

  // -------------------------
  // Print values
  // -------------------------
  Serial.print("Gas: ");
  Serial.print(gasValue);

  Serial.print(" | Distance: ");

  if (distance < 0) {
    Serial.print("NO_ECHO");
  } else {
    Serial.print(distance);
    Serial.print(" cm");
  }

  Serial.println();

  delay(500);
}