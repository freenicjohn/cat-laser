/*
 Uses a 2-axis joystick to control 2 sg90 servos
 Written by Nic John
*/

#include <Servo.h>
  
// Initialize variables
Servo servo_base;  // base axis
Servo servo_tilt;  // tilt axis
float x_reading, y_reading, tilt_command, tilt_force, auto_x, auto_y;
int base_command, modifier, tilt_frequency = 2, rotate_frequency = 2;
float signal_max = 1023.0;
bool laser, on, manual_control, button_state;
double t = 0;

// Set pin numbers
int DO_BASE_PIN = 9;  // base
int DO_TILT_PIN = 8;  // tilt
int DO_LASER_PIN = 6;
int AI_Y_PIN = A1;
int AI_X_PIN = A0;
int DI_SW_PIN = 7;

void setup() {
  // Attach servo pins
  servo_base.attach(DO_BASE_PIN);
  servo_tilt.attach(DO_TILT_PIN);
  
  // Set pin modes
  pinMode(AI_Y_PIN, INPUT);
  pinMode(AI_X_PIN, INPUT);
  pinMode(DI_SW_PIN, INPUT);
  pinMode(DO_LASER_PIN, OUTPUT);
  
  // Begin serial monitor to see values
  Serial.begin(9600);
  Serial.println(F("Starting program..."));
  delay(1000);

  // Set manual or auto control
  manual_control = false;
}

void loop() {
  // button to turn on/off
  if (digitalRead(DI_SW_PIN) == LOW){  // active state
    delay(50);  // debounce button
    if (digitalRead(DI_SW_PIN) == LOW){
      button_state = true;
    }
  }
  if (button_state and digitalRead(DI_SW_PIN) == HIGH){
    if (on){
        on = false;
      }
      else {
        on = true;
      }
    button_state = false;
  }
  
  // manual or auto control
  if (on and manual_control){
    laser = true;
    // read values from joystick
    x_reading = signal_max - analogRead(AI_X_PIN);  // raw signal 0 - 1023
    y_reading = signal_max - analogRead(AI_Y_PIN);  // raw signal 0 - 1023

    // calculate angles for each axis
    tilt_force = sqrt(pow(x_reading - (signal_max/2), 2) + pow(y_reading - (signal_max/2), 2));  // 0 - 50
    tilt_command = cos(tilt_force / (signal_max / 2) * M_PI) * 90;
    base_command = atan2((signal_max/2) - y_reading, (signal_max/2) - x_reading) * 180 / M_PI;

    if (y_reading > signal_max/2){
      tilt_command = 180 - tilt_command;
      base_command = 180 + base_command;
    }
  }
  else if (on and not manual_control) {  // auto control
    laser = true;
    tilt_command = 45 + (sin(tilt_frequency * t/100) * 15);  // 0 - 90
    base_command = 90 + (sin(rotate_frequency * t/100) * 35);
    t ++;  // increment time counter
    if (t > 100.0 * 2 * M_PI) {
      t = 0.0;
      tilt_frequency = int(random(2, 6));  // choose random profiles for tilt and rotation
      rotate_frequency = int(random(2, 12));
    }
  }
  else{
    laser = false;
    tilt_command = 45;
    base_command = 90;
  }

  // send control to servos - don't send if press force isn't over a threshold
  if ((tilt_force > 80) || (manual_control == false)){  
    servo_base.write(base_command);
  }
  servo_tilt.write(tilt_command);
  delay(15);  // waits for the servo to get there

  // laser control
  if (on and laser) {
    digitalWrite(DO_LASER_PIN, HIGH);
  }
  else {
    laser = false;
    digitalWrite(DO_LASER_PIN, LOW);
  }
  
  // print values to serial monitor
  /*Serial.print("X: ");
  Serial.print(x_reading);
  Serial.print("| Y: ");
  Serial.print(y_reading);
  Serial.print("| base: ");
  Serial.print(base_command);
  Serial.print("| tilt: ");
  Serial.println(tilt_command);*/
  Serial.print("t: ");
  Serial.print(t);
  Serial.print("| i: ");
  Serial.print(tilt_frequency);
  Serial.print("| j: ");
  Serial.println(rotate_frequency);
  
}
