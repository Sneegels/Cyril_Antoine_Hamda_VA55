from pybricks.hubs import EV3Brick

class LCDDisplay:
    """
    Afficheur LCD pour le robot EV3.
    """

    def __init__(self):
        self.ev3 = EV3Brick()

    def show_status(self, status_dict):
        """
        Affiche l'état du robot sur l'écran.
        """
        self.ev3.screen.clear()
        lines = []
        for key, value in status_dict.items():
            lines.append(str(key) + ": " + str(value))
        for i, line in enumerate(lines):
            self.ev3.screen.draw_text(10, 20 + i*20, line)