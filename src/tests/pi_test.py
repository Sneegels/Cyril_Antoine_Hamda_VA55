from src.calculs.PI import PIController
import time
from src.config import PI_KP, PI_KI, PI_SETPOINT, PI_SPEED, LOOP_ITERATIONS, LOOP_DELAY

def test_pi_controller(motors, color_sensor, logger, status):
    """Test du contrôleur Proportionnel-Intégral (PI)"""
    print("=== DÉBUT TEST PROPORTIONNEL-INTÉGRAL ===")

    controller = PIController(kp=PI_KP, ki=PI_KI, setpoint=PI_SETPOINT)
    base_speed = PI_SPEED
    start_time = time.time()

    for i in range(LOOP_ITERATIONS):
        reflection = color_sensor.get_reflection()
        correction = controller.compute(reflection)

        # Commande du robot
        motors.drive_base.drive(base_speed, correction)

        # Calculs pour affichage détaillé
        error = controller.setpoint - reflection
        integral = sum(controller.errors)
        proportional_part = controller.kp * error
        integral_part = controller.ki * integral
        left_speed = base_speed - correction
        right_speed = base_speed + correction

        # Mise à jour du statut
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
            right_speed=right_speed,
        )

        # Logging
        logger.log(status.get_status())

        # Affichage console détaillé
        # print(f"PI | Iter: {i:3d} | Refl: {reflection:2d} | P: {proportional_part:+4.0f} | I: {integral_part:+4.0f} | Corr: {correction:+4.0f}")
        time.sleep(LOOP_DELAY)

    motors.drive_base.stop()
    print("=== FIN TEST PROPORTIONNEL-INTÉGRAL ===\n")