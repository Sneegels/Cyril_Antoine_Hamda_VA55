"""
Module implémentant un contrôleur proportionnel (P).
Le contrôleur P produit une correction proportionnelle à l'erreur
entre la consigne et la mesure.
"""

class PController:
    """
    Contrôleur proportionnel simple.
    """

    def __init__(self, kp, setpoint):
        self.kp = kp
        self.setpoint = setpoint

    def compute(self, value):
        """
        Calcule la correction proportionnelle.

        Args:
            value (float): La valeur mesurée

        Returns:
            float: La correction à appliquer
        """
        error = self.setpoint - value
        return self.kp * error
