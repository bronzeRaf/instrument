// Pins
const int ping1 = 13;   // Trigger Pin of Ultrasonic Sensor 1
const int echo1 = 12;   // Echo Pin of Ultrasonic Sensor 1
const int ping2 = 11;   // Trigger Pin of Ultrasonic Sensor 2
const int echo2 = 10;   // Echo Pin of Ultrasonic Sensor 2
const int ping3 = 9;    // Trigger Pin of Ultrasonic Sensor 3
const int echo3 = 8;    // Echo Pin of Ultrasonic Sensor

// Helpers
long max_distance = 1000000; 
long base_value = 
// Previous values
long previous_ultrasonic_1;
long previous_ultrasonic_2;
long previous_ultrasonic_3;
// Current values
long current_ultrasonic_1;
long current_ultrasonic_2;
long current_ultrasonic_3;

void setup() {
  Serial.begin(9600); // Starting Serial Terminal
  setup_ultrasonic_sensors();
  
  previous_ultrasonic_1 = use_ultrasonic_sensor(ping1, echo1);
  previous_ultrasonic_2 = use_ultrasonic_sensor(ping2, echo2);
  previous_ultrasonic_3 = use_ultrasonic_sensor(ping3, echo3);
}

void loop() {
  // Obtain current values
  current_ultrasonic_1 = exclude_outliers(previous_ultrasonic_1, use_ultrasonic_sensor(ping1, echo1), max_distance);
  current_ultrasonic_2 = exclude_outliers(previous_ultrasonic_2, use_ultrasonic_sensor(ping2, echo2), max_distance);
  current_ultrasonic_3 = exclude_outliers(previous_ultrasonic_3, use_ultrasonic_sensor(ping3, echo3), max_distance);

  Serial.print("Sharp: ");
  Serial.print(current_sharp);
  Serial.print(" | Ultrasonic: ");
  Serial.print(current_ultrasonic);
  Serial.print(" | IR: ");
  Serial.print(current_ir);
  Serial.print(" | Base: ");
  Serial.println(current_static);  // prints the value of the sensor to the serial monitor
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
  pinMode(ping1, OUTPUT);
  pinMode(ping2, OUTPUT);
  pinMode(ping3, OUTPUT);
  pinMode(echo1, INPUT);
  pinMode(echo2, INPUT);
  pinMode(echo3, INPUT);
}

long use_ultrasonic_sensor(int pingPin, int echoPin){
  long duration, cm, max_val = 100, min_val = 4;  // Sensor value, cm, max and min
  
  digitalWrite(pingPin, LOW);
  delayMicroseconds(10);
  digitalWrite(pingPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(pingPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  cm = microsecondsToCentimeters(duration);
  
  // Value boundaries
  if(cm > max_val){ cm = max_val; }
  if(cm < min_val){ cm = min_val; }
  return map(cm, min_val, max_val, 0, 255);
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
