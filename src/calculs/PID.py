class PIDController:

    def __init__(self, *, kp, ki, kd, setpoint, max_errors=100):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.errors = []
        self.last_error = 0
        self.max_errors = max_errors

    def compute(self, value):
        error = self.setpoint - value
        self.errors.append(error)
        # Limite la taille de la liste d’erreurs
        if len(self.errors) > self.max_errors:
            self.errors.pop(0)
            print("Warning: Error list exceeded max size, oldest error removed.")
        integral = sum(self.errors)
        derivative = error - self.last_error
        self.last_error = error
        return self.kp * error + self.ki * integral + self.kd * derivative