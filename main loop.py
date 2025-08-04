# Import the ultrasonic class and sleep function
from ultrasonic import Ultrasonic
from time import sleep

# Initialize the ultrasonic sensors (replace with correct GPIO pin numbers)
ultra_front = Ultrasonic(trigger_pin=23, echo_pin=24)
ultra_left = Ultrasonic(trigger_pin=27, echo_pin=22)
ultra_right = Ultrasonic(trigger_pin=5, echo_pin=6)

# Read the distances from the sensors
d_front = ultra_front.read_cm()
d_left = ultra_left.read_cm()
d_right = ultra_right.read_cm()

# Check for an obstacle in front of the robot
if d_front < 6:
    motores.stop()  # Stop the motors
    motores.turn_left(90)  # Turn left 90 degrees
    sleep(2)

    # Move forward while there is an obstacle on the right
    while d_right < 6:
        motores.forward(vel)
    sleep(1)
    motores.stop()
    motores.turn_right(90)
    sleep(2)

    # Move forward until there's space on the right
    while d_right > 6:
        motores.forward(vel)
    # Continue moving forward while there's still an obstacle
    while d_right < 6:
        motores.forward(vel)
    sleep(1)
    motores.stop()
    motores.turn_right(90)

    # Move forward until the line is found again
    while not line_found:
        motores.forward(vel)
    sleep(1)
    motores.stop()
    motores.turn_left(90)

# === Main Navigation Loop ===
def main_loop():
    global green_marks, red_detected
    while True:
        cor = detect_color()
        
        if cor == "Green":
            green_marks += 1
            print(f"[CheckPoint] Green mark #{green_marks}")
            time.sleep(0.5)

        elif cor == "Red" and not red_detected:
            red_detected = True
            print("[End] Red mark found. Stopping.")
            # motores.stop()
            break

        deviation = get_line_deviation()
        correction = pid(deviation)
        print(f"[PID] Deviation: {deviation:.2f}, Correction: {correction:.2f}")

        # motores.set_speed(base + correction, base - correction)
        time.sleep(0.1)


main_loop()
