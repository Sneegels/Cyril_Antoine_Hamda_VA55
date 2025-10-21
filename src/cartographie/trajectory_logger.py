class TrajectoryLogger:
    """
    Permet de stocker et d'exporter la trajectoire du robot (x, y).
    """

    def __init__(self):
        self.positions = []

    def add(self, x, y):
        """Ajoute une position (x, y) à la trajectoire."""
        self.positions.append((x, y))

    def export(self, filename="trajectory.csv"):
        """Exporte la trajectoire dans un fichier CSV."""
        with open(filename, "w") as f:
            for x, y in self.positions:
                f.write(str("{},{}\n".format(x, y)))

    def reset(self):
        """Réinitialise la trajectoire enregistrée."""
        self.positions = []