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

def test_bangbang(motors, color_sensor, logger, sound_light):
    """Test 1: Bang-Bang avec log des erreurs"""
    print("=== TEST 1: BANG-BANG ===")
    sound_light.beep()
    
    controller = BangBangController(threshold=30, delta=60)
    base_speed = 150
    start_time = time.time()
    
    for i in range(200):  # 20 secondes à 10Hz
        reflection = color_sensor.get_reflection()
        error = 30 - reflection  # Erreur par rapport au seuil
        correction = controller.compute(reflection)
        
        left_speed = base_speed - correction
        right_speed = base_speed + correction
        
        # Limiter les vitesses
        left_speed = max(50, min(250, int(left_speed)))
        right_speed = max(50, min(250, int(right_speed)))
        
        # Log des données
        log_data = {
            "test": "bangbang",
            "iteration": i,
            "time": time.time() - start_time,
            "reflection": reflection,
            "error": error,
            "correction": correction,
            "left_speed": left_speed,
            "right_speed": right_speed
        }
        logger.log(log_data)
        
        motors.drive(left_speed, right_speed)
        time.sleep(0.1)  # 10Hz
    
    motors.stop()
    sound_light.flash_leds()
    print("Bang-Bang terminé")

def test_pid_1m_line(motors, color_sensor, logger, sound_light):
    """Test 2: PID sur ligne droite 1 mètre"""
    print("=== TEST 2: PID LIGNE DROITE 1M ===")
    sound_light.beep()
    sound_light.beep()
    
    controller = PIDController(kp=2.0, ki=0.1, kd=0.5, setpoint=25)
    base_speed = 150
    start_time = time.time()
    
    # Compter les tours de roue pour mesurer la distance
    motors.reset()
    target_distance_deg = 1000  # ~1 mètre en degrés de rotation
    iteration = 0
    
    while abs(motors.left_motor.angle()) < target_distance_deg:
        reflection = color_sensor.get_reflection()
        current_distance = abs(motors.left_motor.angle())
        
        error = controller.setpoint - reflection
        correction = controller.compute(reflection)
        
        left_speed = base_speed - correction
        right_speed = base_speed + correction
        
        # Limiter les vitesses
        left_speed = max(50, min(250, int(left_speed)))
        right_speed = max(50, min(250, int(right_speed)))
        
        # Log des données
        log_data = {
            "test": "pid_1m",
            "iteration": iteration,
            "time": time.time() - start_time,
            "reflection": reflection,
            "error": error,
            "correction": correction,
            "distance_deg": current_distance,
            "left_speed": left_speed,
            "right_speed": right_speed
        }
        logger.log(log_data)
        
        motors.drive(left_speed, right_speed)
        iteration += 1
        time.sleep(0.05)  # 20Hz pour plus de précision
    
    motors.stop()
    total_time = time.time() - start_time
    sound_light.flash_leds()
    print("PID 1m terminé - Temps:", total_time, "s")

def test_pid_track(motors, color_sensor, logger, sound_light):
    """Test 3: PID sur tapis de course complet"""
    print("=== TEST 3: PID TAPIS DE COURSE ===")
    sound_light.play_tone(1000, 500)  # Son différent
    
    controller = PIDController(kp=2.5, ki=0.08, kd=0.6, setpoint=25)
    base_speed = 140
    search_counter = 0
    start_time = time.time()
    
    for i in range(800):  # ~80 secondes pour parcours complet
        reflection = color_sensor.get_reflection()
        
        if reflection < 35:  # Sur la ligne noire
            search_counter = 0
            error = controller.setpoint - reflection
            correction = controller.compute(reflection)
            left_speed = base_speed - correction
            right_speed = base_speed + correction
            status = "following"
            
        else:  # Ligne perdue - mode recherche
            search_counter += 1
            error = reflection - 35  # Erreur de sortie de ligne
            correction = 0  # Pas de PID en mode recherche
            
            if search_counter < 15:  # Cherche à droite
                left_speed = 100
                right_speed = -100
                status = "search_right"
            elif search_counter < 45:  # Cherche à gauche
                left_speed = -100
                right_speed = 100
                status = "search_left"
            else:  # Avance et recommence
                search_counter = 0
                left_speed = base_speed
                right_speed = base_speed
                status = "advance"
        
        # Limiter les vitesses
        left_speed = max(-200, min(200, int(left_speed)))
        right_speed = max(-200, min(200, int(right_speed)))
        
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
            "status": status,
            "search_counter": search_counter
        }
        logger.log(log_data)
        
        motors.drive(left_speed, right_speed)
        time.sleep(0.1)  # 10Hz
    
    motors.stop()
    total_time = time.time() - start_time
    sound_light.flash_leds(times=5)
    print("PID Track terminé - Temps:", total_time, "s")

def main():
    """Fonction principale - lance tous les tests du TP"""
    # Initialisation des composants
    status = RobotStatus()
    lcd = LCDDisplay()
    logger = Logger("tp1_logs")  # Dossier spécifique
    color_sensor = ColorSensorWrapper()
    distance_sensor = DistanceSensorWrapper()
    motors = MotorController()
    sound_light = SoundLight()
    
    print("=== DEBUT TP1 - SUIVI DE LIGNE ===")
    sound_light.set_leds()
    
    # Attente avant démarrage
    print("Démarrage dans 3 secondes...")
    time.sleep(3)
    
    # Test 1: Bang-Bang (log des erreurs)
    test_bangbang(motors, color_sensor, logger, sound_light)
    time.sleep(2)
    
    # Test 2: PID ligne droite 1m (log erreurs + temps)
    #test_pid_1m_line(motors, color_sensor, logger, sound_light)
    #time.sleep(2)
    
    # Test 3: PID tapis complet (log erreurs + temps)
    #test_pid_track(motors, color_sensor, logger, sound_light)
    
    # Fin des tests
    sound_light.play_tone(2000, 1000)
    print("=== TP1 TERMINE - TOUS LES LOGS SAUVEGARDES ===")

if __name__ == "__main__":
    main()