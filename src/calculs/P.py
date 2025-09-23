class PController:
    """
    Contrôleur proportionnel simple.
    """

    def __init__(self, kp, setpoint):
        self.kp = kp
        self.setpoint = setpoint

    def compute(self, value):
        error = self.setpoint - value
        return self.kp * error