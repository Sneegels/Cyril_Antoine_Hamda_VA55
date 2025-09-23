#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Stop

class MotorController:
    """
    Classe pour piloter les deux moteurs du robot EV3.
    """

    def __init__(self, left_port=Port.B, right_port=Port.C):
        self.left_motor = Motor(left_port)
        self.right_motor = Motor(right_port)

    def drive(self, left_speed, right_speed):
        """
        Fait tourner les moteurs à des vitesses indépendantes (deg/s).
        """
        self.left_motor.run(left_speed)
        self.right_motor.run(right_speed)

    def forward(self, speed):
        """
        Avance tout droit à la vitesse donnée (deg/s).
        """
        self.drive(speed, speed)

    def rotate(self, angle, speed):
        """
        Tourne sur place d'un certain angle à une vitesse donnée.
        angle > 0 : tourne à droite, angle < 0 : tourne à gauche
        """
        # On peut faire tourner les moteurs en sens opposé pour pivoter
        if angle > 0:
            self.drive(speed, -speed)
        else:
            self.drive(-speed, speed)

    def stop(self, stop_type=Stop.BRAKE):
        """
        Arrête les deux moteurs selon le mode choisi.
        """
        self.left_motor.stop(stop_type)
        self.right_motor.stop(stop_type)

    def reset(self):
        """
        Réinitialise l'angle des deux moteurs.
        """
        self.left_motor.reset_angle(0)
        self.right_motor.reset_angle(0)

    def get_status(self):
        """
        Retourne l'angle actuel des deux moteurs.
        """
        return {
            "left_angle": self.left_motor.angle(),
            "right_angle": self.right_motor.angle()
        }