from core.robot_status import RobotStatus
from core.lcd_display import LCDDisplay
from core.logger import Logger
from sensors.color_sensor import ColorSensorWrapper
from sensors.distance_sensor import DistanceSensorWrapper
from actuators.motor_controller import MotorController

def main():
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
        status.update(distance=distance, color=color)
        lcd.show_status(status.get_status())
        logger.log(status.get_status())
        motors.forward(200)
    
    motors.stop()

if __name__ == "__main__":
    main()