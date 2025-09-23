import time
import os

class Logger:
    """
    Logger CSV pour l'état du robot.
    """

    def __init__(self, log_dir="logs"):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        self.filepath = os.path.join(log_dir, f"log_{timestamp}.csv")

    def log(self, status: dict):
        """
        Ajoute une ligne dans le fichier CSV avec horodatage.
        """
        with open(self.filepath, "a") as f:
            line = f"{time.time()}"
            for value in status.values():
                line += f",{value}"
            f.write(line + "\n")