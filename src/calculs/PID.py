class PIDController:
    """
    Contrôleur PID pour suivi de ligne.
    """

    def __init__(self, kp, ki, kd, setpoint, max_history=10):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.errors = []
        self.max_history = max_history
        self.last_error = 0

    def compute(self, value):
        error = self.setpoint - value
        self.errors.append(error)
        if len(self.errors) > self.max_history:
            self.errors.pop(0)
        integral = sum(self.errors)
        derivative = error - self.last_error
        self.last_error = error
        return self.kp * error + self.ki * integral + self.kd * derivative