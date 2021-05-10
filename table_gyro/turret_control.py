import serial
import time


arduino = serial.Serial(port='COM8', baudrate=115200, timeout=.1)


def write_to_arduino(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    return


def condition_servo_command(cmd):
    cmd = abs(int(cmd))

    if cmd > 180:
        cmd = "180"
    elif cmd < 100 and cmd >= 10:
        cmd = "0" + str(cmd)  # servo commands must always have 3 digits
    elif cmd < 10:
        cmd = "00" + str(cmd)

    return str(cmd)


if __name__ == '__main__':
    while True:
        base = condition_servo_command(input("Enter base deg: "))
        tilt = condition_servo_command(input("Enter tilt deg: "))
        laser = input("Enter 1 for laser on, 0 for off: ")
        write_to_arduino(base + tilt + laser)
