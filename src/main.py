"""
Main module for the line follower robot. This module initializes all required components
and runs the main control loop to demonstrate basic functionality.
"""

from core.robot_status import RobotStatus
from core.lcd_display import LCDDisplay
from core.logger import Logger
from sensors.color_sensor import ColorSensorWrapper
from sensors.distance_sensor import DistanceSensorWrapper
from actuators.motor_controller import MotorController

def main():
    """
    Main function that initializes robot components and runs a basic demo loop.
    The robot will move forward while monitoring color, distance, and updating status.
    """
    status = RobotStatus()
    lcd = LCDDisplay()
    logger = Logger()
    color_sensor = ColorSensorWrapper()
    distance_sensor = DistanceSensorWrapper()
    motors = MotorController()

    # Exemple de boucle principale
    for _ in range(10):
        color = color_sensor.get_color()
        reflection = color_sensor.get_reflection()
        distance = distance_sensor.get_distance()
        status.update(distance=distance, color=color, reflection=reflection)
        lcd.show_status(status.get_status())
        logger.log(status.get_status())
        motors.forward(200)

    motors.stop()

if __name__ == "__main__":
    main()
