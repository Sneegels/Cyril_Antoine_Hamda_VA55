class RobotStatus:
    """
    Stocke l'état courant du robot.
    """

    def __init__(self):
        self.distance = None
        self.color = None
        self.reflection = None
        self.last_error = None

    def update(self, distance=None, color=None, reflection=None, error=None):
        if distance is not None:
            self.distance = distance
        if color is not None:
            self.color = color
        if reflection is not None:
            self.reflection = reflection
        if error is not None:
            self.last_error = error

    def get_status(self):
        return {
            "distance": self.distance,
            "color": self.color,
            "reflection": self.reflection,
            "last_error": self.last_error
        }