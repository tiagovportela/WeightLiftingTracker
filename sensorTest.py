#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tinkerforge.brick_imu_v2 import BrickIMUV2
from tinkerforge.ip_connection import IPConnection
import csv
import time
HOST = "localhost"
PORT = 4223
UID = "6aqRUm"  # Change XXYYZZ to the UID of your IMU Brick 2.0


with open('data.csv', mode='a') as data_file:
    data_writer = csv.writer(
        data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    data_writer.writerow([
        "AccX",
        "AccY",
        "AccZ",
        "MagX",
        "MagY",
        "MagZ",
        "wX",
        "wY",
        "wZ",
        "oX",
        "oY",
        "oZ",
        "time",
        "dt"

    ])

start_time = time.time()
last_time = time.time()
# Callback function for all data callback

last_o_x = 0
last_o_y = 0
last_o_z = 0


def cb_all_data(acceleration, magnetic_field, angular_velocity, euler_angle, quaternion,
                linear_acceleration, gravity_vector, temperature, calibration_status):

    global start_time
    global last_time
    global last_o_x
    global last_o_y
    global last_o_z

    print("Acceleration [X]: " + str(acceleration[0]/100.0) + " m/s²")
    print("Acceleration [Y]: " + str(acceleration[1]/100.0) + " m/s²")
    print("Acceleration [Z]: " + str(acceleration[2]/100.0) + " m/s²")
    print("Magnetic Field [X]: " + str(magnetic_field[0]/16.0) + " µT")
    print("Magnetic Field [Y]: " + str(magnetic_field[1]/16.0) + " µT")
    print("Magnetic Field [Z]: " + str(magnetic_field[2]/16.0) + " µT")
    print("Angular Velocity [X]: " + str(angular_velocity[0]/16.0) + " °/s")
    print("Angular Velocity [Y]: " + str(angular_velocity[1]/16.0) + " °/s")
    print("Angular Velocity [Z]: " + str(angular_velocity[2]/16.0) + " °/s")
    print("Euler Angle [Heading]: " + str(euler_angle[0]/16.0) + " °")
    print("Euler Angle [Roll]: " + str(euler_angle[1]/16.0) + " °")
    print("Euler Angle [Pitch]: " + str(euler_angle[2]/16.0) + " °")
    print("Quaternion [W]: " + str(quaternion[0]/16383.0))
    print("Quaternion [X]: " + str(quaternion[1]/16383.0))
    print("Quaternion [Y]: " + str(quaternion[2]/16383.0))
    print("Quaternion [Z]: " + str(quaternion[3]/16383.0))
    print("Linear Acceleration [X]: " +
          str(linear_acceleration[0]/100.0) + " m/s²")
    print("Linear Acceleration [Y]: " +
          str(linear_acceleration[1]/100.0) + " m/s²")
    print("Linear Acceleration [Z]: " +
          str(linear_acceleration[2]/100.0) + " m/s²")
    print("Gravity Vector [X]: " + str(gravity_vector[0]/100.0) + " m/s²")
    print("Gravity Vector [Y]: " + str(gravity_vector[1]/100.0) + " m/s²")
    print("Gravity Vector [Z]: " + str(gravity_vector[2]/100.0) + " m/s²")
    print("Temperature: " + str(temperature) + " °C")
    print("Calibration Status: " + format(calibration_status, "08b"))
    print("")

    t = time.time() - start_time

    dt = t - last_time

    last_time = t

    acc_x = acceleration[0]/100.0
    acc_y = acceleration[1]/100.0
    acc_z = acceleration[2]/100.0

    mag_x = magnetic_field[0]/16.0
    mag_y = magnetic_field[1]/16.0
    mag_z = magnetic_field[2]/16.0

    w_x = angular_velocity[0]/16.0
    w_y = angular_velocity[1]/16.0
    w_z = angular_velocity[2]/16.0

    o_x = last_o_x + w_x * dt
    o_y = last_o_y + w_y * dt
    o_z = last_o_z + w_z * dt

    last_o_x = o_x
    last_o_y = o_y
    last_o_z = o_z

    with open('data.csv', mode='a') as data_file:
        data_writer = csv.writer(
            data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        data_writer.writerow([
            acceleration[0]/100.0,
            acceleration[1]/100.0,
            acceleration[2]/100.0,
            magnetic_field[0]/16.0,
            magnetic_field[1]/16.0,
            magnetic_field[2]/16.0,
            angular_velocity[0]/16.0,
            angular_velocity[1]/16.0,
            angular_velocity[2]/16.0,
            o_x,
            o_y,
            o_z,
            t,
            dt

        ])


if __name__ == "__main__":
    ipcon = IPConnection()  # Create IP connection
    imu = BrickIMUV2(UID, ipcon)  # Create device object

    ipcon.connect(HOST, PORT)  # Connect to brickd
    # Don't use device before ipcon is connected

    # Register all data callback to function cb_all_data
    imu.register_callback(imu.CALLBACK_ALL_DATA, cb_all_data)

    # Set period for all data callback to 0.1s (100ms)
    imu.set_all_data_period(100)

    input("Press key to exit\n")  # Use raw_input() in Python 2
    ipcon.disconnect()
