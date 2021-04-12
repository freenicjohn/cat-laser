/*
 Uses a 2-axis joystick to control 2 sg90 servos
 Written by Nic John
*/

#include <Servo.h>
  
// Initialize variables
Servo servo_base;  // base axis
Servo servo_tilt;  // tilt axis
int x_reading = 0;
int y_reading = 0;
int tilt_command = 0;
int base_command = 0;
bool tilt_forward;
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
  x_reading = map(analogRead(AI_X_PIN), 0, 1023, 50, -50);
  y_reading = map(analogRead(AI_Y_PIN), 0, 1023, 50, -50);
  Serial.print("X: ");
  Serial.print(x_reading);
  Serial.print(" | Y: ");
  Serial.println(y_reading);

  // determine direction of tilt
  tilt_forward = (y_reading > 0);

  // calculate angles for each axis
  press_force = sqrt(pow(x_reading, 2) + pow(y_reading, 2));
  if (tilt_forward){
    tilt_command = map(press_force, 0, 50, 90, 180);
    base_command = atan2(y_reading, x_reading) * 180 / M_PI;
  }
  else {
    tilt_command = map(press_force, 0, 50, 90, 0);
    base_command = 180 + atan2(y_reading, x_reading) * 180 / M_PI;
  }

  // send control to servos
  servo_base.write(base_command);
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
