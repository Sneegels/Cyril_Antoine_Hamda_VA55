from src.calculs.P import PController
import time
from src.config import P_KP, P_SETPOINT, P_SPEED, LOOP_ITERATIONS, LOOP_DELAY

def test_proportional(motors, color_sensor, logger, status):
    """Test du contrôleur Proportionnel (P)"""
    print("=== DÉBUT TEST PROPORTIONNEL ===")

    controller = PController(kp=P_KP, setpoint=P_SETPOINT)
    base_speed = P_SPEED
    start_time = time.time()

    for i in range(LOOP_ITERATIONS):
        reflection = color_sensor.get_reflection()
        correction = controller.compute(reflection)

        # Commande du robot
        motors.drive_base.drive(base_speed, correction)

        # Calculs pour affichage et logging
        error = controller.setpoint - reflection
        left_speed = base_speed - correction
        right_speed = base_speed + correction

        # Mise à jour du statut
        status.update(
            controller_type="Proportional",
            iteration=i,
            time=time.time() - start_time,
            reflection=reflection,
            error=error,
            correction=correction,
            setpoint=controller.setpoint,
            speed=base_speed,
            left_speed=left_speed,
            right_speed=right_speed,
        )

        # Logging
        logger.log(status.get_status())

        # Affichage console
        # print(f"P | Iter: {i:3d} | Refl: {reflection:2d} | Err: {error:+3.0f} | Corr: {correction:+4.0f}")
        time.sleep(LOOP_DELAY)

    motors.drive_base.stop()
    print("=== FIN TEST PROPORTIONNEL ===\n")