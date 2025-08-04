# Import the DistanceSensor class from the gpiozero library
from gpiozero import DistanceSensor

class Ultrasonic:
    def __init__(self, trigger_pin, echo_pin):
        # Initialize the ultrasonic sensor with trigger and echo pins
        self.ultra = DistanceSensor(echo=echo_pin, trigger=trigger_pin)

    def read_cm(self):
        """Reads the distance in centimeters."""
        return self.ultra.distance * 100  # Converts from meters to centimeters
