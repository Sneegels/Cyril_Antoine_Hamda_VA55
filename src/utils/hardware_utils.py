from pybricks.parameters import Port
from pybricks.ev3devices import ColorSensor
import time
from src.actuators.motor_controller import MotorController
from src.sensors.color_sensor import ColorSensorWrapper
import src.config as config


def find_color_sensor():
    """Trouve automatiquement le port du capteur de couleur"""
    print("=== RECHERCHE DU CAPTEUR DE COULEUR ===")
    ports = [Port.S1, Port.S2, Port.S3, Port.S4]

    for port in ports:
        try:
            sensor = ColorSensor(port)
            reflection = sensor.reflection()
            # print(f"✅ CAPTEUR TROUVÉ sur {port} - Réflexion: {reflection}")
            return port
        except Exception as e:
            print("❌ Pas de capteur")

    print("⚠️ AUCUN CAPTEUR TROUVÉ !")
    return None


def test_motor_balance():
    """Test individuel des moteurs pour vérifier l'équilibrage"""
    print("=== TEST D'ÉQUILIBRAGE DES MOTEURS ===")
    motors = MotorController(
        config.LEFT_MOTOR_PORT, config.RIGHT_MOTOR_PORT, config.WHEEL_DIAMETER, config.AXLE_TRACK
    )

    # Test moteur gauche
    print("🔄 Test moteur GAUCHE à 300 deg/s pendant 2s...")
    motors.left_motor.run(300)
    time.sleep(2)
    motors.drive_base.stop()
    time.sleep(1)

    # Test moteur droit
    print("🔄 Test moteur DROIT à 300 deg/s pendant 2s...")
    motors.right_motor.run(300)
    time.sleep(2)
    motors.drive_base.stop()

    print("✅ Test d'équilibrage terminé\n")


def calibrate_color_sensor():
    """Calibration du capteur de couleur sur blanc et noir"""
    print("=== CALIBRATION DU CAPTEUR DE COULEUR ===")
    color_sensor = ColorSensorWrapper(config.COLOR_SENSOR_PORT)

    print("📍 Placez le robot sur la LIGNE NOIRE et appuyez sur le bouton central...")
    # TODO: Ajouter attente bouton
    time.sleep(3)  # Temporaire
    black_reflection = color_sensor.get_reflection()
    # print(f"⚫ Réflexion NOIR: {black_reflection}")

    print("📍 Placez le robot sur le BLANC et appuyez sur le bouton central...")
    # TODO: Ajouter attente bouton
    time.sleep(3)  # Temporaire
    white_reflection = color_sensor.get_reflection()
    # print(f"⚪ Réflexion BLANC: {white_reflection}")

    optimal_threshold = (black_reflection + white_reflection) / 2
    # print(f"🎯 Seuil optimal calculé: {optimal_threshold:.1f}")
    # print(f"🔧 Ajustez OPTIMAL_THRESHOLD = {optimal_threshold:.0f} dans la configuration\n")

    return black_reflection, white_reflection, optimal_threshold


def print_configuration():
    """Affiche la configuration actuelle"""
    print("=== CONFIGURATION ACTUELLE ===")
    # print(f"Hardware:")
    # print(f"  - Moteur gauche: {LEFT_MOTOR_PORT}")
    # print(f"  - Moteur droit: {RIGHT_MOTOR_PORT}")
    # print(f"  - Capteur couleur: {COLOR_SENSOR_PORT}")
    # print(f"DriveBase:")
    # print(f"  - Diamètre roues: {WHEEL_DIAMETER} mm")
    # print(f"  - Écartement: {AXLE_TRACK} mm")
    # print(f"Contrôleurs:")
    # print(f"  - Seuil optimal: {OPTIMAL_THRESHOLD}")
    # print(f"  - Bang-Bang: Δ={BANGBANG_DELTA}, V={BANGBANG_SPEED} mm/s")
    # print(f"  - Proportionnel: Kp={P_KP}, V={P_SPEED} mm/s")
    # print(f"  - PI: Kp={PI_KP}, Ki={PI_KI}, V={PI_SPEED} mm/s")
    # print(f"  - PID: Kp={PID_KP}, Ki={PID_KI}, Kd={PID_KD}, V={PID_SPEED} mm/s")
    print()