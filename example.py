from __future__ import print_function
import time
from single_tb9051ftg_rpi import Motor, Motors, MAX_SPEED

# Create a Motor and Motors object
motor1 = Motor(pwm1_pin=12, pwm2_pin=13, en_pin=4, enb_pin=5, diag_pin=6)
motors = Motors(motor1)

# Define a custom exception to raise if a fault is detected.
class DriverFault(Exception):
    def __init__(self, driver_num):
        self.driver_num = driver_num

def raiseIfFault():
    if motors.motor1.getFault():
        raise DriverFault(1)
    # if motors.motor2.getFault():
    #     raise DriverFault(2)

# Set up sequences of motor speeds.
test_forward_speeds = list(range(0, MAX_SPEED, 1)) + \
  [MAX_SPEED] * 200 + list(range(MAX_SPEED, 0, -1)) + [0]

test_reverse_speeds = list(range(0, -MAX_SPEED, -1)) + \
  [-MAX_SPEED] * 200 + list(range(-MAX_SPEED, 0, 1)) + [0]

try:
    motors.setSpeeds(0)         # removed the second motor speed

    print("Motor 1 forward")
    for s in test_forward_speeds:
        motors.motor1.setSpeed(s)
        raiseIfFault()
        time.sleep(0.002)

    print("Motor 1 reverse")
    for s in test_reverse_speeds:
        motors.motor1.setSpeed(s)
        raiseIfFault()
        time.sleep(0.002)

    # Disable the drivers for half a second.
    motors.disable()
    time.sleep(0.5)
    motors.enable()

    # print("Motor 2 forward")
    # for s in test_forward_speeds:
    #     motors.motor2.setSpeed(s)
    #     raiseIfFault()
    #     time.sleep(0.002)

    # print("Motor 2 reverse")
    # for s in test_reverse_speeds:
    #     motors.motor2.setSpeed(s)
    #     raiseIfFault()
    #     time.sleep(0.002)

except DriverFault as e:
    print("Driver %s fault!" % e.driver_num)

finally:
    # Stop the motors, even if there is an exception
    # or the user presses Ctrl+C to kill the process.
    motors.forceStop()
