# Integrated navigation module using MPU6050 and TCS34725 with PID and markers
import time
import math
import board
import busio
import adafruit_mpu6050
import adafruit_tcs34725
from simple_pid import PID 

# === Sensor Setup ===
i2c = busio.I2C(board.SCL, board.SDA)
mpu = adafruit_mpu6050.MPU6050(i2c)
tcs = adafruit_tcs34725.TCS34725(i2c)
tcs.integration_time = 100
tcs.gain = 4

# === PID Setup ===
setpoint = 0.3  # Randoom values
pid = PID(1.0, 0.02, 0.01, setpoint=setpoint)
pid.output_limits = (-1.0, 1.0)

# === Variables for symbolic localization ===
green_marks = 0
red_detected = False

# === Gyroscope Function ===
def read_gyro_z():
    return mpu.gyro[2]

# === Motor turning functions using MPU ===
def turn_left(target_deg):
    angle = 0
    prev = time.monotonic()
    print("Turning left...")
    

    while angle < target_deg:
        now = time.monotonic()
        delta = now - prev
        prev = now
        angle += math.degrees(read_gyro_z()) * delta
        time.sleep(0.01)
    
    # motores.stop()
    print("Stop")

def turn_right(target_deg):
    angle = 0
    prev = time.monotonic()
    print("Turning right...")
    # motores.girar_direita()

    while angle < target_deg:
        now = time.monotonic()
        delta = now - prev
        prev = now
        angle += -math.degrees(read_gyro_z()) * delta
        time.sleep(0.01)
    
    # motores.stop()
    print("Stop")

# === Color Sensor Functions ===
def detect_color():
    r, g, b = tcs.color_rgb_bytes
    print(f"RGB = {r}, {g}, {b}")
    if g > r and g > b and g > 100:
        return "Green"
    elif r > g and r > b and r > 100:
        return "Red"
    elif b > r and b > g and b > 100:
        return "Blue"
    elif r > 200 and g > 200 and b > 200:
        return "White"
    return "Unknown"

def get_line_deviation():
    r, g, b = tcs.color_rgb_bytes
    brightness = (r + g + b) / 3
    deviation = 1.0 - brightness / 255.0  # 0 = white, 1 = black line
    return deviation
