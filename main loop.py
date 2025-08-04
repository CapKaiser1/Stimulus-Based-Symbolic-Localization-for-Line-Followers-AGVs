from time import sleep, time
from ultrasonic import Ultrasonic
from navigation import (
    detect_color, get_line_deviation, pid,
    turn_left, turn_right
)

# === Sensor Initialization ===
ultra_front = Ultrasonic(trigger_pin=23, echo_pin=24)
ultra_left = Ultrasonic(trigger_pin=27, echo_pin=22)
ultra_right = Ultrasonic(trigger_pin=5, echo_pin=6)

# === System State ===
green_marks = 0
red_detected = False
mode = "in_operation"  # "in_operation" or "returning_to_rest"
line_found = False  # Controlled externally
current_aisle = None
base_speed = 50  # Placeholder for motor base speed

# Aisle memory map: number of marks -> left/right action
aisle_memory = {
    1: {"left": "Aisle 1 Left", "right": "Aisle 1 Right"},
    2: {"left": "Aisle 2 Left", "right": "Aisle 2 Right"},
    3: {"left": "Aisle 3 Left", "right": "Aisle 3 Right"},
}

# === Obstacle Avoidance ===
def obstacle_avoidance():
    d_front = ultra_front.read_cm()
    d_right = ultra_right.read_cm()

    if d_front < 6:
        print("[Obstacle] Detected ahead. Executing avoidance...")
        motores.stop()
        turn_left(90)
        sleep(2)

        while ultra_right.read_cm() < 6:
            motores.forward(base_speed)
        sleep(1)

        motores.stop()
        turn_right(90)
        sleep(2)

        while ultra_right.read_cm() > 6:
            motores.forward(base_speed)

        while ultra_right.read_cm() < 6:
            motores.forward(base_speed)
        sleep(1)

        motores.stop()
        turn_right(90)

        while not line_found:
            motores.forward(base_speed)

        sleep(1)
        motores.stop()
        turn_left(90)

# === Aisle Logic ===
def handle_aisle_logic(mark_count, direction):
    global current_aisle

    if mark_count in aisle_memory:
        action = aisle_memory[mark_count][direction]
        print(f"[Aisle] Detected: {action}")
        current_aisle = action
        if direction == "left":
            turn_left(90)
        elif direction == "right":
            turn_right(90)

# === Return to Rest Area ===
def return_to_rest():
    global green_marks, red_detected, mode

    print("[Mode] Switching to 'returning_to_rest'")
    mode = "returning_to_rest"

    while not red_detected:
        color = detect_color()

        if color == "Green":
            green_marks -= 1
            print(f"[Return] Decrementing Green Mark: {green_marks}")
            sleep(0.5)

        elif color == "Red":
            print("[Rest Area] Red Mark detected. Stopping.")
            red_detected = True
            motores.stop()
            break

        deviation = get_line_deviation()
        correction = pid(deviation)
        motores.set_speed(base_speed + correction, base_speed - correction)
        sleep(0.1)

# === Main Navigation Loop ===
def main_loop():
    global green_marks, red_detected, mode

    while True:
        obstacle_avoidance()

        color = detect_color()

        if color == "Green":
            if mode == "in_operation":
                green_marks += 1
                print(f"[Checkpoint] Green Mark: {green_marks}")
                handle_aisle_logic(green_marks, direction="left")  # Example: always left for now

            elif mode == "returning_to_rest":
                green_marks -= 1
                print(f"[Return] Green Mark decremented to {green_marks}")

            sleep(0.5)

        elif color == "Red" and not red_detected:
            print("[Rest] Red mark detected. Stopping.")
            red_detected = True
            motores.stop()
            break

        deviation = get_line_deviation()
        correction = pid(deviation)
        print(f"[PID] Deviation: {deviation:.2f}, Correction: {correction:.2f}")
        motores.set_speed(base_speed + correction, base_speed - correction)
        sleep(0.1)

# === Start Robot ===
if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        motores.stop()
        print("\n[System] Interrupted by user.")


#For next versions:
#1. Include motors and pwm.
#2. Include PID Output for motors.
#3. Include pick and place application.
#4. Include load detection with Esp32cam.
