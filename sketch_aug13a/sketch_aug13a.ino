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

  long duration = pulseIn(echoPin, HIGH);

  float distance = duration * 0.0343 / 2;

  // -------------------------
  // Print values
  // -------------------------
  Serial.print("Gas: ");
  Serial.print(gasValue);

  Serial.print(" | Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  delay(500);
}