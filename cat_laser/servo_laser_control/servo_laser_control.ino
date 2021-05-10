/* Controls laser turret via serial communications with PC (Pyserial)
 *  Command format is servo1servo2laser
 *  i.e. "1234561" means "servo 1 to 123, servo 2 to 456, and laser on
 *  
 *  Expects button switch to turn servo control on/off
 *  
 *  Written by Nic John 5/9/2021
 */

# include <Servo.h>

// Initialize variables
Servo servo_base;  // base axis
Servo servo_tilt;  // tilt axis
String input;
int base_cmd, tilt_cmd;
bool laser_cmd, button_state, on;

// Set pin numbers
int DO_BASE_PIN = 9;  // base
int DO_TILT_PIN = 8;  // tilt
int DO_LASER_PIN = 6;
int DI_SW_PIN = 7;

void setup() {
  // Attach servo pins
  servo_base.attach(DO_BASE_PIN);
  servo_tilt.attach(DO_TILT_PIN);
  
  // Set pin modes
  pinMode(DI_SW_PIN, INPUT);
  pinMode(DO_LASER_PIN, OUTPUT);

  // Start serial monitor
  Serial.begin(115200);
  Serial.setTimeout(1);
  delay(1000);
}

void loop() {
  // Handle button logic
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
  
  if (on){
    // Get base/tilt commands from PC
    if (Serial.available()){
      input = Serial.readString();
      base_cmd = input.substring(0,3).toInt();
      tilt_cmd = input.substring(3,6).toInt();
      laser_cmd = (input.substring(6,7).toInt() == 1);
    
      // Servo control
      servo_base.write(base_cmd);
      servo_tilt.write(tilt_cmd);
    
      // Laser control
      if (laser_cmd) {digitalWrite(DO_LASER_PIN, HIGH);}
      else {digitalWrite(DO_LASER_PIN, LOW);}

      Serial.print(1);  // Tell the PC if we're on
    }
  }
}
