
# 📂 Project: Stimulus-Based Symbolic Localization for Line-Following AGVs in Warehouse Load Dispatch without Global Mapping

> A Python-based warehouse robot using symbolic floor markers, MPU6050, TCS34725, and ultrasonic sensors for smart navigation on Raspberry Pi.

---

## 📁 Current Files

### 1. `navigation.py`

Contains navigation functions using the MPU6050 gyroscope and TCS34725 color sensor:

- `turn_left(angle)`: Rotates the robot to the left by a given angle.
- `turn_right(angle)`: Rotates the robot to the right by a given angle.
- `detect_color()`: Detects floor color ("green", "red", "white", "unknown").
- Green checkpoint tracking and red endpoint detection.
- State variable: `"working"` or `"returning"`.

---

### 2. `ultrasonic.py`

Reusable class for front and side ultrasonic sensors:

```python
class Ultrasonic:
    def __init__(trigger_pin, echo_pin)
    def read_cm()
```
Used in `main_loop.py` for obstacle avoidance and line reacquisition.

---

### 3. `main_loop.py`

Main control loop for the robot:

- Initializes ultrasonic sensors.
- Performs obstacle avoidance.
- Detects color markings and adjusts behavior.
- Manages checkpoints and state transitions.
- Handles memory-based entry/exit of aisles.

---

## ⚙️ Required Libraries

Install using:

```bash
pip install adafruit-circuitpython-mpu6050
pip install adafruit-circuitpython-tcs34725
pip install simple-pid
sudo apt install python3-gpiozero python3-rpi.gpio
```

---

## 🧠 For next versions:

1. Include motor and PWM control.
2. Add PID output to drive motors.
3. Implement pick and place application.
4. Integrate load detection with ESP32-CAM.

---