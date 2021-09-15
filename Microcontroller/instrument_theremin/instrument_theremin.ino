// Pins
const int pingPin = 13; // Trigger Pin of Ultrasonic Sensor
const int echoPin = 12; // Echo Pin of Ultrasonic Sensor
int staticPin = 5;       // analog pin used to measure the static voltage
int sharpPin = 0;       // analog pin used to connect the sharp sensor
int irPin = 3;          // analog pin used to connect the ir sensor
// Helpers
long max_distance = 10000; 
// Previous values
long previous_static;
long previous_ultrasonic;
long previous_sharp;
long previous_ir;
long previous_random;
// Current values
long current_static;
long current_ultrasonic;
long current_sharp;
long current_ir;
long current_random;


void setup() {
  Serial.begin(9600); // Starting Serial Terminal
  setup_ultrasonic_sensor();
  previous_static = use_static();
  previous_ultrasonic = use_ultrasonic_sensor();
  previous_sharp = use_sharp_sensor();
  previous_ir = use_ir_sensor();
  previous_random = use_random();
}

void loop() {
  // Obtain current values
  current_static = exclude_outliers(previous_static, use_static(), max_distance);
  current_ultrasonic = exclude_outliers(previous_ultrasonic, use_ultrasonic_sensor(), max_distance);
  current_sharp = exclude_outliers(previous_sharp, use_sharp_sensor(), max_distance);
  current_ir = exclude_outliers(previous_ir, use_ir_sensor(), max_distance);
  current_random = exclude_outliers(previous_random, use_random(), max_distance);

  Serial.println(current_ultrasonic);  // prints the value of the sensor to the serial monitor
  delay(800);                      // wait for this much time before printing next value

  // Replace previous values
  previous_static = current_static;
  previous_ultrasonic = current_ultrasonic;
  previous_sharp = current_sharp;
  previous_ir = current_ir;
  previous_random = current_random;
} 


// _____________________Ultrasonic Sensor_______________________
void setup_ultrasonic_sensor(){
   pinMode(pingPin, OUTPUT);
   pinMode(echoPin, INPUT);
}

long use_ultrasonic_sensor(){
   long duration, cm;
   
   digitalWrite(pingPin, LOW);
   delayMicroseconds(10);
   digitalWrite(pingPin, HIGH);
   delayMicroseconds(10);
   digitalWrite(pingPin, LOW);
   duration = pulseIn(echoPin, HIGH);
   cm = microsecondsToCentimeters(duration);
   return map(cm, 0, 125, 0, 255);
}
// _____________________________________________________________


// _______________________Static Voltage________________________
long use_static(){
  long static_val = 0;                 // Sharp sensor value
  static_val = analogRead(staticPin);  // reads the value of the sharp sensor
  return map(static_val, 0, 1023, 0, 255);
}
// _____________________________________________________________

// _______________________Sharp Sensor__________________________
long use_sharp_sensor(){
   long sharp_val, volts;                 // Sharp sensor value
   sharp_val = analogRead(sharpPin);//*0.0048828125;   // reads the value of the sharp sensor
//   return 13*pow(sharp_val, -1);
  return map(sharp_val, 0, 1023, 0, 255);
}
// _____________________________________________________________

// __________________________IR Sensor__________________________
long use_ir_sensor(){
   long ir_val = 0;              // IR sensor value
   ir_val = analogRead(irPin);   // reads the value of the ir sensor
   return map(ir_val, 0, 1023, 0, 255);
}
// _____________________________________________________________


// ________________________Helpers______________________________
long microsecondsToCentimeters(long microseconds) {
   return microseconds / 29 / 2;
}

long exclude_outliers(long previous, long current, long max_distance){
  if(abs(previous - current) > max_distance){ return previous; }
  else{ return current; }
}
// _____________________________________________________________


// ________________________Random_______________________________

long use_random(){
  long x = random(0, 255);
  return x;
}
// _____________________________________________________________
