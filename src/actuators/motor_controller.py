#!/usr/bin/env pybricks-micropython
"""
Module pour contrôler les moteurs du robot EV3.
"""

from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Stop

class MotorController:

    def __init__(self, left_port, right_port):
        # Initialisation des moteurs sur les ports spécifiés
        self.left_motor = Motor(left_port)
        self.right_motor = Motor(right_port)

    def forward(self, speed):
        # Avance en ligne droite à une vitesse donnée.
        self.drive(speed, speed)

    def rotate(self, angle, speed):
        # Fait pivoter le robot d'un angle donné (en degrés) à une vitesse spécifique.
        if angle > 0:
            self.drive(speed, -speed)
        else:
            self.drive(-speed, speed)

    def stop(self, stop_type=Stop.BRAKE):
        # Arrête les moteurs avec le type d'arrêt spécifié.
        if stop_type == Stop.BRAKE:
            self.left_motor.brake()
            self.right_motor.brake()
        elif stop_type == Stop.COAST:
            self.left_motor.stop()
            self.right_motor.stop()

    def reset(self):
        # Réinitialise les compteurs d'angle des moteurs à zéro.
        self.left_motor.reset_angle(0)
        self.right_motor.reset_angle(0)

    
    def drive(self, vitesse_entrainement, vitesse_rotation):
        # Calcule et applique les vitesses aux moteurs pour avancer et tourner.
        left_speed = vitesse_entrainement - vitesse_rotation
        right_speed = vitesse_entrainement + vitesse_rotation
        self.left_motor.run(left_speed)
        self.right_motor.run(right_speed)


    def get_status(self):
        # Retourne l'état actuel des moteurs (angles).
        return {
            "left_angle": self.left_motor.angle(),
            "right_angle": self.right_motor.angle()
        }
