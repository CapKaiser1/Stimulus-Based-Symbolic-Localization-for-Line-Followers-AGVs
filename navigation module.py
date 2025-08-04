# Integrated navigation module using MPU6050 and TCS34725

import time
import math
import board
import busio
import adafruit_mpu6050
import adafruit_tcs34725

# === Sensor Setup ===

# I2C communication
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize sensors
mpu = adafruit_mpu6050.MPU6050(i2c)
tcs = adafruit_tcs34725.TCS34725(i2c)
tcs.integration_time = 100  # in ms
tcs.gain = 4

# === Gyroscope Functions ===
def read_gyro_z():
    """Reads Z-axis value from gyroscope."""
    return mpu.gyro[2]

def turn_left(target_angle_deg):
    angle = 0.0
    prev_time = time.monotonic()
    print("[MPU] Turning left...")
    # motors.turn_left()

    while angle < target_angle_deg:
        curr_time = time.monotonic()
        delta_t = curr_time - prev_time
        prev_time = curr_time

        deg_per_sec = math.degrees(read_gyro_z())
        angle += deg_per_sec * delta_t

        time.sleep(0.01)

    print("[MPU] Stopping motors")
    # motors.stop()

def turn_right(target_angle_deg):
    angle = 0.0
    prev_time = time.monotonic()
    print("[MPU] Turning right...")
    # motors.turn_right()

    while angle < target_angle_deg:
        curr_time = time.monotonic()
        delta_t = curr_time - prev_time
        prev_time = curr_time

        deg_per_sec = -math.degrees(read_gyro_z())  # Invert signal
        angle += deg_per_sec * delta_t

        time.sleep(0.01)

    print("[MPU] Stopping motors")
    # motors.stop()

# === Color Sensor Functions ===
def detect_color():
    """Returns the detected color name based on RGB ratio."""
    r, g, b = tcs.color_rgb_bytes
    print(f"[TCS] R: {r}, G: {g}, B: {b}")

    if g > r and g > b and g > 100:
        return "Green"
    elif r > g and r > b and r > 100:
        return "Red"
    elif b > r and b > g and b > 100:
        return "Blue"
    elif r > 200 and g > 200 and b > 200:
        return "White"
    else:
        return "Unknown"