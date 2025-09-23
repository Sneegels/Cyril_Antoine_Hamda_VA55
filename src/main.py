#!/usr/bin/env pybricks-micropython

import time
from core.robot_status import RobotStatus
from core.lcd_display import LCDDisplay
from core.logger import Logger
from sensors.color_sensor import ColorSensorWrapper
from sensors.distance_sensor import DistanceSensorWrapper
from actuators.motor_controller import MotorController
from actuators.sound_light import SoundLight
from calculs.bangbang import BangBangController
from calculs.P import PController
from calculs.PI import PIController
from calculs.PID import PIDController

# def test_bangbang(motors, color_sensor, logger, sound_light):
#     """Test 1: Bang-Bang avec log des erreurs"""
#     print("=== TEST 1: BANG-BANG ===")
#     sound_light.beep()
#     
#     controller = BangBangController(threshold=30, delta=60)
#     base_speed = 150
#     start_time = time.time()
#     
#     for i in range(200):  # 20 secondes à 10Hz
#         reflection = color_sensor.get_reflection()
#         error = 30 - reflection  # Erreur par rapport au seuil
#         correction = controller.compute(reflection)
#         
#         left_speed = base_speed - correction
#         right_speed = base_speed + correction
#         
#         # Limiter les vitesses
#         left_speed = max(50, min(250, int(left_speed)))
#         right_speed = max(50, min(250, int(right_speed)))
#         
#         # Log des données
#         log_data = {
#             "test": "bangbang",
#             "iteration": i,
#             "time": time.time() - start_time,
#             "reflection": reflection,
#             "error": error,
#             "correction": correction,
#             "left_speed": left_speed,
#             "right_speed": right_speed
#         }
#         logger.log(log_data)
#         
#         motors.drive(left_speed, right_speed)
#         time.sleep(0.1)  # 10Hz
#     
#     motors.stop()
#     sound_light.flash_leds()
#     print("Bang-Bang terminé")

# def test_pid_1m_line(motors, color_sensor, logger, sound_light):
#     """Test 2: PID sur ligne droite 1 mètre"""
#     print("=== TEST 2: PID LIGNE DROITE 1M ===")
#     sound_light.beep()
#     sound_light.beep()
#     
#     controller = PIDController(kp=2.0, ki=0.1, kd=0.5, setpoint=25)
#     base_speed = 150
#     start_time = time.time()
#     
#     # Compter les tours de roue pour mesurer la distance
#     motors.reset()
#     target_distance_deg = 1000  # ~1 mètre en degrés de rotation
#     iteration = 0
#     
#     while abs(motors.left_motor.angle()) < target_distance_deg:
#         reflection = color_sensor.get_reflection()
#         current_distance = abs(motors.left_motor.angle())
#         
#         error = controller.setpoint - reflection
#         correction = controller.compute(reflection)
#         
#         left_speed = base_speed - correction
#         right_speed = base_speed + correction
#         
#         # Limiter les vitesses
#         left_speed = max(50, min(250, int(left_speed)))
#         right_speed = max(50, min(250, int(right_speed)))
#         
#         # Log des données
#         log_data = {
#             "test": "pid_1m",
#             "iteration": iteration,
#             "time": time.time() - start_time,
#             "reflection": reflection,
#             "error": error,
#             "correction": correction,
#             "distance_deg": current_distance,
#             "left_speed": left_speed,
#             "right_speed": right_speed
#         }
#         logger.log(log_data)
#         
#         motors.drive(left_speed, right_speed)
#         iteration += 1
#         time.sleep(0.05)  # 20Hz pour plus de précision
#     
#     motors.stop()
#     total_time = time.time() - start_time
#     sound_light.flash_leds()
#     print("PID 1m terminé - Temps:", total_time, "s")

def test_pid_track(motors, color_sensor, logger, sound_light):
    """Test 3: PID sur tapis de course complet"""
    print("=== TEST PID SUIVI DE LIGNE ===")
    sound_light.play_tone(1000, 500)
    
    controller = PIDController(kp=3.0, ki=0.1, kd=0.5, setpoint=25)
    base_speed = 180  # Vitesse augmentée mais raisonnable
    start_time = time.time()
    
    for i in range(500):
        reflection = color_sensor.get_reflection()
        
        # UNE SEULE LOGIQUE PID - TOUJOURS LA MÊME
        error = controller.setpoint - reflection
        correction = controller.compute(reflection)
        
        # Application directe de la correction
        left_speed = base_speed - correction
        right_speed = base_speed + correction
        
        # Déterminer statut pour les logs
        if reflection < 20:
            status = "on_black"
        elif reflection > 40:
            status = "on_white"  
        else:
            status = "on_edge"
        
        # Limiter les vitesses - VALEURS SÛRES
        left_speed = max(50, min(250, int(left_speed)))
        right_speed = max(50, min(250, int(right_speed)))
        
        print("L: " + str(left_speed) + ", R: " + str(right_speed))

        # Log des données
        log_data = {
            "test": "pid_track",
            "iteration": i,
            "time": time.time() - start_time,
            "reflection": reflection,
            "error": error,
            "correction": correction,
            "left_speed": left_speed,
            "right_speed": right_speed,
            "status": status
        }
        logger.log(log_data)
        
        motors.drive(left_speed, right_speed)
        time.sleep(0.08)  # Légèrement plus rapide: 12.5Hz
    
    motors.stop()
    total_time = time.time() - start_time
    sound_light.flash_leds(times=5)
    print("PID Track terminé - Temps:", total_time, "s")

def main():
    """Fonction principale - PID uniquement"""
    # Initialisation des composants
    status = RobotStatus()
    lcd = LCDDisplay()
    color_sensor = ColorSensorWrapper()
    distance_sensor = DistanceSensorWrapper()
    motors = MotorController()
    sound_light = SoundLight()
    
    print("=== PID SUIVI DE LIGNE ===")
    sound_light.set_leds()
    
    # Attente avant démarrage
    print("Démarrage dans 3 secondes...")
    time.sleep(3)
    
    # Seulement le PID Track
    logger_track = Logger("logs_pid_only")
    test_pid_track(motors, color_sensor, logger_track, sound_light)
    print("Log PID terminé. Fichier:", logger_track.filepath)
    
    print("=== PID TERMINE ===")

if __name__ == "__main__":
    main()