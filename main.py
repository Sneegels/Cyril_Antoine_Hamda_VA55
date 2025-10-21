#!/usr/bin/env pybricks-micropython

from src.tests.bangbang_test import test_bangbang
from src.tests.p_test import test_proportional
from src.tests.pi_test import test_pi_controller
from src.tests.pid_test import test_pid_controller
import src.config as config
import src.utils.hardware_utils as hw_utils
from src.actuators.motor_controller import MotorController
from src.sensors.color_sensor import ColorSensorWrapper
from src.sensors.gyro_sensor import GyroSensorWrapper
from src.core.logger import Logger
from src.core.robot_status import RobotStatus
from pybricks.parameters import Port
from pybricks.ev3devices import ColorSensor


def main():

    """Fonction principale - Exécute les tests des contrôleurs"""
    print("DÉMARRAGE DU PROGRAMME DE SUIVI DE LIGNE")
    print("=" * 50)

    # Affichage de la configuration
    hw_utils.print_configuration()

    # Initialisation des composants
    print("Initialisation des composants...")
    motors = MotorController(
        config.LEFT_MOTOR_PORT, config.RIGHT_MOTOR_PORT, config.WHEEL_DIAMETER, config.AXLE_TRACK
    )
    color_sensor = ColorSensorWrapper(config.COLOR_SENSOR_PORT)
    gyro_sensor = GyroSensorWrapper(config.GYRO_SENSOR_PORT)
    robot_status = RobotStatus()

    # Initialisation des loggers
    print("Initialisation des loggers...")
    #logger_bb = Logger("logs_bangbang")
    #logger_p = Logger("logs_proportional")
    #logger_pi = Logger("logs_pi")
    logger_pid = Logger("logs_pid")

    print("Initialisation terminée\n")

    # Exécution des tests (décommenter selon besoin)

    # Test Bang-Bang
    # test_bangbang(motors, color_sensor, logger_bb, robot_status)

    # Test Proportionnel
    # test_proportional(motors, color_sensor, logger_p, robot_status)

    # Test Proportionnel-Intégral
    # test_pi_controller(motors, color_sensor, logger_pi, robot_status)

    # Test Proportionnel-Intégral-Dérivé
    test_pid_controller(motors, color_sensor, gyro_sensor, logger_pid, robot_status)

    # Affichage des fichiers de logs générés
    print("FICHIERS DE LOGS GÉNÉRÉS :")
    # print(f"  - Bang-Bang: {logger_bb.filepath}")
    # print(f"  - Proportionnel: {logger_p.filepath}")
    # print(f"  - PI: {logger_pi.filepath}")
    # print(str("  - PID: {logger_pid.filepath}"))

    print("\nPROGRAMME TERMINÉ")

if __name__ == "__main__":
    main()