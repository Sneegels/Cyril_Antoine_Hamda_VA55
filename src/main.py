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

    setpoint = 50  # distance cible en cm
    Kp = 2         # gain proportionnel
    Ki = 0.1       # gain intégral
    Kd = 0.5       # gain dérivé
    integral = 0
    previous_error = 0

    # Exemple de boucle principale
    for _ in range(10):
        color = color_sensor.get_color()
        reflection = color_sensor.get_reflection()
        distance = distance_sensor.get_distance()
        error = setpoint - distance # P
        integral += error # PI
        derivative = error - previous_error # PID

        speed_p = Kp * error
        speed_i = Ki * integral
        speed_d = Kd * derivative
        speed_pi = speed_p + speed_i
        speed_pid = speed_p + speed_i + speed_d
        speed = max(0, min(255, int(speed_p)))  # vitesse entre 0 et 255

        status.update(distance=distance, color=color, reflection=reflection, speed=speed)
        lcd.show_status(status.get_status())
        logger.log(status.get_status())
        motors.forward(speed)

    motors.stop()

if __name__ == "main":
    main()
