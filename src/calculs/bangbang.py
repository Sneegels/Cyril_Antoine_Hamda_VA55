class BangBangController:
    """
    Contrôleur Bang-Bang pour suivi de ligne.
    """

    def __init__(self, threshold, delta):
        self.threshold = threshold  # valeur de consigne (ex: 50%)
        self.delta = delta          # amplitude de correction

    def compute(self, value):
        """
        Retourne la correction à appliquer selon la mesure.
        """
        if value < self.threshold:
            # Trop à gauche (sur le noir)
            return -self.delta
        else:
            # Trop à droite (sur le blanc)
            return self.delta