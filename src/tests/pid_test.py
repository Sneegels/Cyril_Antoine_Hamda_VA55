from src.calculs.PID import PIDController
from src.calculs.kalman_filter import KalmanFilter
import time
import math
from src.config import PID_KP, PID_KI, PID_KD, PID_SETPOINT, PID_SPEED, LOOP_ITERATIONS, LOOP_DELAY
from src.cartographie.trajectory_logger import TrajectoryLogger

def test_pid_controller(motors, color_sensor, gyro_sensor, logger, status):
    """Test du contrôleur Proportionnel-Intégral-Dérivé (PID)"""
    print("=== DÉBUT TEST PROPORTIONNEL-INTÉGRAL-DÉRIVÉ ===")

    controller = PIDController(kp=PID_KP, ki=PID_KI, kd=PID_KD, setpoint=PID_SETPOINT)
    base_speed = PID_SPEED
    start_time = time.time()

    trajectory_brute = TrajectoryLogger()
    trajectory_kalman = TrajectoryLogger()
    theta_gyro, theta_drivebase = 0, 0
    x_brute, y_brute, theta_brute = 0, 0, 0
    x_kalman, y_kalman, theta_kalman = 0, 0, 0

    #kalman_filter_pid = KalmanFilter(1.0, 1.0, 0.01)
    kalman_filter_gyro = KalmanFilter(1.0, 1.0, 0.01)
    kalman_filter_drivebase = KalmanFilter(1.0, 1.0, 0.01)

    for i in range(LOOP_ITERATIONS):
        reflection = color_sensor.get_reflection()
        correction = controller.compute(reflection)

        # Commande du robot
        motors.drive_base.drive(base_speed, correction)

        # Calculs pour affichage des 3 composantes PID
        error = controller.setpoint - reflection
        integral = sum(controller.errors)
        derivative = error - controller.last_error if i > 0 else 0
        proportional_part = controller.kp * error
        integral_part = controller.ki * integral
        derivative_part = controller.kd * derivative
        left_speed = base_speed - correction
        right_speed = base_speed + correction

        # Mise à jour du statut
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
            right_speed=right_speed,
        )

        # Logging
        logger.log(status.get_status())

        distance = motors.drive_base.distance()

        #angle_pid = correction * LOOP_DELAY
        #theta_pid = math.radians(angle_pid)
        #kalman_theta_pid = kalman_filter_pid.update(theta_pid)

        angle_gyro = gyro_sensor.get_angle()
        theta_gyro = math.radians(angle_gyro)
        filtered_theta_gyro = kalman_filter_gyro.update(theta_gyro)

        angle_drivebase = motors.drive_base.angle()
        theta_drivebase = math.radians(angle_drivebase)
        #filtered_theta_drivebase = kalman_filter_drivebase.update(theta)

        # Trajectoire brute (sans Kalman)
        theta_brute += theta_gyro
        x_brute += math.cos(theta_brute) * distance
        y_brute += math.sin(theta_brute) * distance
        trajectory_brute.add(x_brute, y_brute)

        # Trajectoire filtrée (avec Kalman (gyro ou drivebase))
        theta_kalman += filtered_theta_gyro # filtered_theta_drivebase
        x_kalman += math.cos(theta_kalman) * distance
        y_kalman += math.sin(theta_kalman) * distance
        trajectory_kalman.add(x_kalman, y_kalman)

        motors.drive_base.reset()
        
        print(str(x_brute) + ", " + str(y_brute) + " BRUTE")
        print(str(x_kalman) + ", " + str(y_kalman) + " KALMAN")

        # Affichage console avec les 3 composantes
        # print(f"PID | Iter: {i:3d} | P: {proportional_part:+4.0f} | I: {integral_part:+4.0f} | D: {derivative_part:+4.0f} | Corr: {correction:+4.0f}")
        time.sleep(LOOP_DELAY)

    trajectory_brute.export("trajectory_brute.csv")
    trajectory_kalman.export("trajectory_kalman.csv")
    motors.drive_base.stop()
    print("=== FIN TEST PROPORTIONNEL-INTÉGRAL-DÉRIVÉ ===\n")