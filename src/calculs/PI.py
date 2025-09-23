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
        error = self.setpoint - value
        self.errors.append(error)
        if len(self.errors) > self.max_history:
            self.errors.pop(0)
        integral = sum(self.errors)
        return self.kp * error + self.ki * integral