/*
 Uses a 2-axis joystick to control 2 sg90 servos
 Written by Nic John
*/

#include <Servo.h>
  
// Initialize variables
Servo servox;  // x axis
Servo servoy;  // y axis
int servox_pos;  // servo x command position
int servoy_pos;  // servo y command position
int x_reading = 0;
int y_reading = 0;
int x_command = 0;
int y_command = 0;

// Set pin numbers
int DO_X_PIN = 9;
int DO_Y_PIN = 8;
int AI_Y_PIN = A0;
int AI_X_PIN = A1;

void setup() {
  // Attach servo pins
  servox.attach(DO_X_PIN);
  servoy.attach(DO_Y_PIN);
  
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
  x_reading = analogRead(AI_X_PIN);
  y_reading = analogRead(AI_Y_PIN);
  x_command = map(x_reading, 0, 1023, 0, 180);
  y_command = map(y_reading, 0, 1023, 0, 180); 
  Serial.print("X: ");
  Serial.print(x_command);
  Serial.print(" | Y: ");
  Serial.println(y_command);

  // send control to servos
  servox.write(x_command);
  servoy.write(y_command);
  delay(15);  // waits for the servo to get there
  
}
