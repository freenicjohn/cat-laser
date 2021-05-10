# Control laser turret by sending commands to the arduino which controls it directly.
# To use this class in the main program, just instantiate a turret object and call object.command(base, tilt, laser)
# don't forget to use object.close() when done with it to close the serial connection.
# Written by Nic John 2021.

import serial
import time


class Turret:

    def __init__(self):
        """ Initialize a turret object"""
        self.arduino = serial.Serial(port='COM8', baudrate=115200, timeout=.1)
        self.is_on = False

    def check_connection(self):
        """ DON'T CALL THIS FUNCTION
        To check if the turret is on, use self.is_on
        Reads from serial buffer - is called automatically upon writing
        """
        inp = self.arduino.read()
        self.is_on = (inp == b'1')
        return self.is_on

    def write_to_arduino(self, x):
        """ Command to arduino is parsed as follows:
            first three digits = base turret position (0-180 deg)
            second three digits = tilt turret position (0-180 deg)
            last digit = laser (1=on/0=off)
        """
        self.arduino.write(bytes(x, 'utf-8'))
        time.sleep(0.05)
        self.check_connection()

    def command(self, base_lcl, tilt_lcl, laser_lcl):
        """ Takes three commands, formats them, and sends them to the arduino"""
        base_lcl = condition_servo_command(base_lcl)
        tilt_lcl = condition_servo_command(tilt_lcl)
        self.write_to_arduino(base_lcl + tilt_lcl + laser_lcl)

    def close(self):
        """ Closes the serial port """
        self.arduino.close()


def condition_servo_command(cmd):
    """ Conditions turret commands to always be 3 digits"""
    cmd = abs(int(cmd))
    if cmd > 180:
        cmd = "180"
    elif 100 > cmd >= 10:
        cmd = "0" + str(cmd)
    elif cmd < 10:
        cmd = "00" + str(cmd)

    return str(cmd)


if __name__ == '__main__':
    laser_turret = Turret()

    while True:
        base = input("Enter base deg: ")
        if base == "q":
            break
        tilt = input("Enter tilt deg: ")
        laser = input("Enter 1 for laser on, 0 for off: ")
        laser_turret.command(base, tilt, laser)
        print(laser_turret.is_on)
    laser_turret.close()
