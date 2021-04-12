/*
 Uses a 2-axis joystick to control 2 sg90 servos
 Written by Nic John
*/

#include <Servo.h>
  
// Initialize variables
Servo servo_base;  // base axis
Servo servo_tilt;  // tilt axis
float x_reading = 0;
float y_reading = 0;
float tilt_command = 0.0;
int base_command = 0;
float signal_max = 1023.0;
float press_force = 0.0;

// Set pin numbers
int DO_BASE_PIN = 9;  // base
int DO_TILT_PIN = 8;  // tilt
int AI_Y_PIN = A1;
int AI_X_PIN = A0;

void setup() {
  // Attach servo pins
  servo_base.attach(DO_BASE_PIN);
  servo_tilt.attach(DO_TILT_PIN);
  
  // Set analog input pin modes
  pinMode(AI_Y_PIN, INPUT);
  pinMode(AI_X_PIN, INPUT);
  
  // Begin serial monitor to see values
  Serial.begin(9600);
  Serial.println(F("Starting program..."));
  delay(1000);
}

void loop() {
  // read values from joystick
  x_reading = signal_max - analogRead(AI_X_PIN);  // raw signal 0 - 1023
  y_reading = signal_max - analogRead(AI_Y_PIN);  // raw signal 0 - 1023
  Serial.print("X: ");
  Serial.print(x_reading);
  Serial.print(" | Y: ");
  Serial.println(y_reading);

  // calculate angles for each axis
  press_force = sqrt(pow(x_reading - (signal_max/2), 2) + pow(y_reading - (signal_max/2), 2));  // 0 - 50
  tilt_command = cos(press_force / (signal_max / 2) * M_PI) * 90;
  base_command = atan2((signal_max/2) - y_reading, (signal_max/2) - x_reading) * 180 / M_PI;
  
  if (y_reading > signal_max/2){
    tilt_command = 180 - tilt_command ;
    base_command = 180 + base_command;
  }

  // send control to servos - don't send if press force isn't over a threshold
  if (press_force > 80){  
    servo_base.write(base_command);
  }
  servo_tilt.write(tilt_command);
  delay(15);  // waits for the servo to get there

  Serial.print("base: ");
  Serial.print(base_command);
  Serial.print(" | tilt: ");
  Serial.println(tilt_command);
  Serial.print("press_force: ");
  Serial.print(press_force);
  Serial.print(" | tilt: ");
  Serial.println(tilt_command);
  
}
