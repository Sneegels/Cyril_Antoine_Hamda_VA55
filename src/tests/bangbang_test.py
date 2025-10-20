from src.calculs.bangbang import BangBangController
from src.config import BANGBANG_THRESHOLD, BANGBANG_DELTA, BANGBANG_SPEED, LOOP_ITERATIONS, LOOP_DELAY

import time

def test_bangbang(motors, color_sensor, logger, status):
    """Test du contrôleur Bang-Bang (tout ou rien)"""
    print("=== DÉBUT TEST BANG-BANG ===")

    controller = BangBangController(threshold=BANGBANG_THRESHOLD, delta=BANGBANG_DELTA)
    base_speed = BANGBANG_SPEED
    start_time = time.time()

    for i in range(LOOP_ITERATIONS):
        reflection = color_sensor.get_reflection()
        correction = controller.compute(reflection)

        # Commande du robot avec DriveBase
        motors.drive_base.drive(base_speed, correction)

        # Calcul des vitesses individuelles pour affichage
        left_speed = base_speed - correction
        right_speed = base_speed + correction

        # Mise à jour du statut
        status.update(
            controller_type="BangBang",
            iteration=i,
            time=time.time() - start_time,
            reflection=reflection,
            error=None,
            correction=correction,
            speed=base_speed,
            left_speed=left_speed,
            right_speed=right_speed,
        )

        # Logging
        logger.log(status.get_status())

        # Affichage console
        # print(f"BB | Iter: {i:3d} | Refl: {reflection:2d} | Corr: {correction:+4.0f}")
        time.sleep(LOOP_DELAY)

    motors.drive_base.stop()
    print("=== FIN TEST BANG-BANG ===\n")