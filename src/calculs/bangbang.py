"""
Module implémentant un contrôleur Bang-Bang pour le suivi de ligne.
Le contrôleur Bang-Bang est la forme la plus simple de contrôle, alternant
entre deux états selon que la mesure est au-dessus ou en-dessous d'un seuil.
"""

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
        # Trop à droite (sur le blanc)
        return self.delta
