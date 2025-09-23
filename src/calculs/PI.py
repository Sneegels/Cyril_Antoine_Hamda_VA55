"""
Module implémentant un contrôleur PI (Proportionnel Intégral).
Le contrôleur PI combine deux actions :
- P : correction proportionnelle à l'erreur
- I : correction proportionnelle à l'intégrale de l'erreur
"""

class PIController:
    """
    Contrôleur proportionnel-intégral.
    """

    def __init__(self, kp, ki, setpoint, max_history=10):
        self.kp = kp
        self.ki = ki
        self.setpoint = setpoint
        self.errors = []
        self.max_history = max_history

    def compute(self, value):
        """
        Calcule la correction PI.

        Args:
            value (float): La valeur mesurée

        Returns:
            float: La correction combinée P+I à appliquer
        """
        error = self.setpoint - value
        self.errors.append(error)
        if len(self.errors) > self.max_history:
            self.errors.pop(0)
        integral = sum(self.errors)
        return self.kp * error + self.ki * integral
