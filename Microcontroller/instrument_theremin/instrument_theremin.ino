const int pingPin = 13; // Trigger Pin of Ultrasonic Sensor
const int echoPin = 12; // Echo Pin of Ultrasonic Sensor
int sharpPin = 0;       // analog pin used to connect the sharp sensor
int irPin = 3;          // analog pin used to connect the ir sensor
int x ;                 // Random number


void setup() {
   Serial.begin(9600); // Starting Serial Terminal
   setup_ultrasonic_sensor();
}

void loop() {
//   use_ultrasonic_sensor();
//   use_sharp_sensor();
   use_ir_sensor();
//   use_random();
}


// _____________________Ultrasonic Sensor_______________________
void setup_ultrasonic_sensor(){
   pinMode(pingPin, OUTPUT);
   pinMode(echoPin, INPUT);
}

void use_ultrasonic_sensor(){
   long duration, cm;
   
   digitalWrite(pingPin, LOW);
   delayMicroseconds(10);
   digitalWrite(pingPin, HIGH);
   delayMicroseconds(10);
   digitalWrite(pingPin, LOW);
   duration = pulseIn(echoPin, HIGH);
   cm = microsecondsToCentimeters(duration);
   Serial.println(cm);
   delay(800);
}
// _____________________________________________________________


// _______________________Sharp Sensor__________________________
void use_sharp_sensor(){
   int sharp_val = 0;                  // Sharp sensor value
   sharp_val = analogRead(sharpPin);  // reads the value of the sharp sensor
   Serial.println(sharp_val);          // prints the value of the sensor to the serial monitor
   delay(800);                         // wait for this much time before printing next value
}
// _____________________________________________________________

// __________________________IR Sensor__________________________
void use_ir_sensor(){
   int ir_val = 0;              // IR sensor value
   ir_val = analogRead(irPin);  // reads the value of the ir sensor
   Serial.println(ir_val);      // prints the value of the sensor to the serial monitor
   delay(800);                  // wait for this much time before printing next value
}
// _____________________________________________________________


// ________________________Helpers______________________________
long microsecondsToCentimeters(long microseconds) {
   return microseconds / 29 / 2;
}
// _____________________________________________________________


// ________________________Random_______________________________

void use_random(){
  x = random(0, 125);
  Serial.println(x);
  delay(800);
}
// _____________________________________________________________
