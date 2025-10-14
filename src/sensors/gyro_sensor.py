from pybricks.ev3devices import GyroSensor
from pybricks.parameters import Port

class GyroSensorWrapper:
    def __init__(self, port):
        # Initialisation du capteur gyroscope
        self.sensor = GyroSensor(port)
        self.reset_angle()

    def get_angle(self):
        # Retourne l'angle absolu mesuré par le gyroscope (en degrés)
        return self.sensor.angle()

    def get_angular_velocity(self):
        # Retourne la vitesse angulaire (en degrés/s)
        return self.sensor.speed()

    def reset_angle(self, angle=0):
        # Réinitialise l'angle du gyroscope à une valeur donnée (par défaut 0)
        self.sensor.reset_angle(angle)