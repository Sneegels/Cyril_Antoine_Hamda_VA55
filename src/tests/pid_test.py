from src.calculs.PID import PIDController
from src.calculs.kalman_filter import KalmanFilter
import time
import math
from src.config import PID_KP, PID_KI, PID_KD, PID_SETPOINT, PID_SPEED, LOOP_ITERATIONS, LOOP_DELAY

def test_pid_controller(motors, color_sensor, gyro_sensor, logger, status):
    """Test du contrôleur Proportionnel-Intégral-Dérivé (PID)"""
    print("=== DÉBUT TEST PROPORTIONNEL-INTÉGRAL-DÉRIVÉ ===")

    controller = PIDController(kp=PID_KP, ki=PID_KI, kd=PID_KD, setpoint=PID_SETPOINT)
    base_speed = PID_SPEED
    start_time = time.time()

    theta = 0
    x = 0
    y = 0

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

        angle_pid = correction * LOOP_DELAY
        theta_pid = math.radians(angle_pid)
        kalman_filter_pid = KalmanFilter(1.0, 1.0, 0.01)
        kalman_theta_pid = kalman_filter_pid.update(math.radians(angle_pid))

        angle_gyro = gyro_sensor.get_angle()
        theta_gyro = math.radians(angle_gyro)
        kalman_filter_gyro = KalmanFilter(1.0, 1.0, 0.01)
        kalman_theta_gyro = kalman_filter_gyro.update(math.radians(angle_gyro))

        angle = motors.drive_base.angle()
        theta += math.radians(angle)
        kalman_filter = KalmanFilter(1.0, 1.0, 0.01)
        kalman_theta = kalman_filter.update(math.radians(angle))

        x += math.cos(theta) * distance
        y += math.sin(theta) * distance
        motors.drive_base.reset()
        print(str(x) + ", " + str(y))

        # Affichage console avec les 3 composantes
        # print(f"PID | Iter: {i:3d} | P: {proportional_part:+4.0f} | I: {integral_part:+4.0f} | D: {derivative_part:+4.0f} | Corr: {correction:+4.0f}")
        time.sleep(LOOP_DELAY)

    motors.drive_base.stop()
    print("=== FIN TEST PROPORTIONNEL-INTÉGRAL-DÉRIVÉ ===\n")