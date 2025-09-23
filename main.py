#!/usr/bin/env pybricks-micropython

import time
from actuators.motor_controller import MotorController
from sensors.color_sensor import ColorSensorWrapper
from calculs.bangbang import BangBangController
from calculs.P import PController
from calculs.PI import PIController
from calculs.PID import PIDController
from core.logger import Logger
from core.robot_status import RobotStatus
from pybricks.parameters import Port

# =============================================================================
# CONFIGURATION DU ROBOT
# =============================================================================
LEFT_MOTOR_PORT = Port.B
RIGHT_MOTOR_PORT = Port.C
COLOR_SENSOR_PORT = Port.S3

def test_bangbang(motors, color_sensor, logger, status):
    # Test 1: Bang-Bang simple avec log
    print("BANG-BANG")
    
    controller = BangBangController(threshold=25, delta=40)
    base_speed = 150  # vitesse_entrainement
    
    for i in range(200):
        reflection = color_sensor.get_reflection()
        
        # Calcul de la correction Bang-Bang
        correction = controller.compute(reflection)  # vitesse_rotation
        
        # Utilisation de drive()
        motors.drive(base_speed, correction)
        
        # Pour l'affichage, on peut calculer les vitesses individuelles
        left_speed = base_speed - correction
        right_speed = base_speed + correction
        
        status.update(
            controller_type="bangbang",
            iteration=i,
            time=time.time() - start_time,
            reflection=reflection,
            error=None,
            correction=correction,
            speed=base_speed,
            left_speed=left_speed,
            right_speed=right_speed
        )
        
        # Log des données
        logger.log(status.get_status())
        
        print("BB | Iter: " + str(i) + " | Refl: " + str(reflection) + " | Corr: " + str(correction))
        time.sleep(0.1)
    
    motors.stop()
    print("BANG-BANG FIN")

def test_proportional(motors, color_sensor, logger, status):
    # Test 2: Contrôleur Proportionnel (P)
    print("PROPORTIONNEL")
    
    # Calcul kp basé sur Bang-Bang : kp = delta / erreur_max
    # Si delta=40 et erreur_max≈20, alors kp=2.0
    controller = PController(kp=2.0, setpoint=45)  # 45 = gris optimal
    base_speed = 150  # Même vitesse que Bang-Bang
    
    for i in range(200):  # 20 secondes
        reflection = color_sensor.get_reflection()
        
        # δ(n) = kp * e(n)
        correction = controller.compute(reflection)
        
        motors.drive(base_speed, correction)

        # Mise à jour du status
        error = controller.setpoint - reflection
        left_speed = base_speed - correction
        right_speed = base_speed + correction
        
        status.update(
            controller_type="P",
            iteration=i,
            time=time.time() - start_time,
            reflection=reflection,
            error=error,
            correction=correction,
            setpoint=controller.setpoint,
            speed=base_speed,
            left_speed=left_speed,
            right_speed=right_speed
        )
        
        logger.log(status.get_status())
        
        print("P | Iter: " + str(i) + " | Refl: " + str(reflection) + " | Err: " + str(error) + " | Corr: " + str(correction))
        time.sleep(0.1)
    
    motors.stop()
    print("PROPORTIONNEL FIN")

def test_pi_controller(motors, color_sensor, logger, status):
    # Test 3: Contrôleur Proportionnel-Intégral (PI)
    print("PORTIONNEL-INTÉGRAL")
    
    controller = PIController(kp=2.0, ki=0.05, setpoint=45)
    base_speed = 150
    
    for i in range(200):  # 20 secondes
        reflection = color_sensor.get_reflection()
        
        # δ(n) = kp*e(n) + ki*∑e(n)
        correction = controller.compute(reflection)
        
        motors.drive(base_speed, correction)
        
        # Affichage détaillé
        error = controller.setpoint - reflection
        integral = sum(controller.errors)
        proportional_part = controller.kp * error
        integral_part = controller.ki * integral
        left_speed = base_speed - correction
        right_speed = base_speed + correction
        
        status.update(
            controller_type="PI",
            iteration=i,
            time=time.time() - start_time,
            reflection=reflection,
            error=error,
            correction=correction,
            setpoint=controller.setpoint,
            integral_error=integral,
            speed=base_speed,
            left_speed=left_speed,
            right_speed=right_speed
        )
        
        logger.log(status.get_status())
        
        print("PI | Iter: " + str(i) + " | Refl: " + str(reflection) + " | P: " + str(int(proportional_part)) + " | I: " + str(int(integral_part)) + " | Corr: " + str(int(correction)))
        time.sleep(0.1)
    
    motors.stop()
    print("PORTIONNEL-INTÉGRAL FIN")

def test_pid_controller(motors, color_sensor, logger, status):
    # Test 4: Contrôleur Proportionnel-Intégral-Dérivé (PID)
    print("PROPORTIONNEL-INTÉGRAL-DÉRIVÉ")
    
    controller = PIDController(kp=2.0, ki=0.05, kd=0.5, setpoint=45)
    base_speed = 150
    
    for i in range(200):  # 20 secondes
        reflection = color_sensor.get_reflection()
        
        # δ(n) = kp*e(n) + ki*∑e(n) + kd*[e(n)-e(n-1)]
        correction = controller.compute(reflection)
        
        motors.drive(base_speed, correction)
        
        # Affichage détaillé des 3 composantes
        error = controller.setpoint - reflection
        integral = sum(controller.errors)
        derivative = error - controller.last_error if i > 0 else 0
        proportional_part = controller.kp * error
        integral_part = controller.ki * integral
        derivative_part = controller.kd * derivative
        left_speed = base_speed - correction
        right_speed = base_speed + correction
        
        status.update(
            controller_type="PID",
            iteration=i,
            time=time.time() - start_time,
            reflection=reflection,
            error=error,
            correction=correction,
            setpoint=controller.setpoint,
            integral_error=integral,
            derivative_error=derivative,
            speed=base_speed,
            left_speed=left_speed,
            right_speed=right_speed
        )
        
        logger.log(status.get_status())
        
        print("PID | Iter: " + str(i) + " | P: " + str(int(proportional_part)) + " | I: " + str(int(integral_part)) + " | D: " + str(int(derivative_part)) + " | Corr: " + str(int(correction)))
        time.sleep(0.1)
    
    motors.stop()
    print("PROPORTIONNEL-INTÉGRAL-DÉRIVÉ FIN")

def main():
    # Initialisation des composants
    motors = MotorController(LEFT_MOTOR_PORT, RIGHT_MOTOR_PORT)
    color_sensor = ColorSensorWrapper(COLOR_SENSOR_PORT)
    robot_status = RobotStatus()

    logger_bb = Logger("logs_bangbang")
    logger_p = Logger("logs_proportional") 
    logger_pi = Logger("logs_pi")
    logger_pid = Logger("logs_pid")
    
    # Test Bang-Bang
    test_bangbang(motors, color_sensor, logger_bb, robot_status)

    # Test Proportionnel
    test_proportional(motors, color_sensor, logger_p, robot_status)

    # Test Proportionnel-Intégral
    test_pi_controller(motors, color_sensor, logger_pi, robot_status)

    # Test Proportionnel-Intégral-Dérivé
    test_pid_controller(motors, color_sensor, logger_pid, robot_status)

    print("\nFICHIERS DE LOGS GÉNÉRÉS :")
    print("Bang-Bang:", logger_bb.filepath)
    print("Proportional:", logger_p.filepath)
    print("PI:", logger_pi.filepath)
    print("PID:", logger_pid.filepath)

if __name__ == "__main__":
    main()