import time
import os

class Logger:
    """
    Logger CSV pour l'état du robot.
    """

    def __init__(self, log_dir="logs"):
        try:
            os.mkdir(log_dir)
        except:
            pass  # Le dossier existe déjà
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        self.filepath = log_dir + "/log_" + timestamp + ".csv"
        self.first_log = True  # Pour écrire les en-têtes

    def log(self, status: dict):
        """
        Ajoute une ligne dans le fichier CSV avec horodatage.
        """
        with open(self.filepath, "a") as f:
            if self.first_log:
                # Écrire les en-têtes CSV
                headers = ",".join(status.keys())
                f.write("timestamp," + headers + "\n")
                self.first_log = False
            
            # Écrire les données
            line = str(time.time())
            for value in status.values():
                line += "," + str(value)
            f.write(line + "\n")