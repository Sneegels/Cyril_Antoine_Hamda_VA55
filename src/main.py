#!/usr/bin/env pybricks-micropython

from core.robot_status import RobotStatus
from core.lcd_display import LCDDisplay
from core.logger import Logger
from sensors.color_sensor import ColorSensorWrapper
from sensors.distance_sensor import DistanceSensorWrapper
from actuators.motor_controller import MotorController
from calculs.PID import PIDController  # Import de ta classe PID

def main():
    status = RobotStatus()
    lcd = LCDDisplay()
    logger = Logger()
    color_sensor = ColorSensorWrapper()
    distance_sensor = DistanceSensorWrapper()
    motors = MotorController()

    # Initialiser le contrôleur PID pour suivre la ligne
    pid_controller = PIDController(
        kp=3.0,
        ki=0.1,
        kd=0.5,
        setpoint=15  # valeur cible pour rester sur la ligne noire
    )
    
    base_speed = 150       # vitesse de base
    
    # Exemple de boucle principale
    for _ in range(50):
        color = color_sensor.get_color()
        reflection = color_sensor.get_reflection()
        distance = distance_sensor.get_distance()
        
        # Calcul de la correction avec le PID
        correction = pid_controller.compute(reflection)
        
        # Vitesses des moteurs (gauche et droite)
        left_speed = base_speed - correction
        right_speed = base_speed + correction
        
        # Limiter les vitesses
        left_speed = max(50, min(300, int(left_speed)))
        right_speed = max(50, min(300, int(right_speed)))
        
        print("Reflection:", reflection, "Correction:", correction, "Left:", left_speed, "Right:", right_speed)

        status.update(distance=distance, color=color, reflection=reflection, left_speed=left_speed, right_speed=right_speed)
        lcd.show_status(status.get_status())
        logger.log(status.get_status())
        
        motors.drive(left_speed, right_speed)

    motors.stop()

if __name__ == "__main__":
    main()