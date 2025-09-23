"""
Module implémentant un contrôleur PID (Proportionnel Intégral Dérivé).
Le contrôleur PID combine trois actions :
- P : correction proportionnelle à l'erreur
- I : correction proportionnelle à l'intégrale de l'erreur
- D : correction proportionnelle à la dérivée de l'erreur
"""

class PIDController:
    """
    Contrôleur PID pour suivi de ligne.
    """

    def __init__(self, *, kp, ki, kd, setpoint, max_history=10):
        """
        Initialise le contrôleur PID.

        Args:
            kp (float): Gain proportionnel
            ki (float): Gain intégral
            kd (float): Gain dérivé
            setpoint (float): Valeur de consigne
            max_history (int, optional): Taille de l'historique pour l'intégrale. Defaults to 10.
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.errors = []
        self.max_history = max_history
        self.last_error = 0

    def compute(self, value):
        """
        Calcule la correction PID.

        Args:
            value (float): La valeur mesurée

        Returns:
            float: La correction combinée P+I+D à appliquer
        """
        error = self.setpoint - value
        self.errors.append(error)
        if len(self.errors) > self.max_history:
            self.errors.pop(0)
        integral = sum(self.errors)
        derivative = error - self.last_error
        self.last_error = error
        return self.kp * error + self.ki * integral + self.kd * derivative
