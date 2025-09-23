from pybricks.hubs import EV3Brick
from pybricks.parameters import Color

class SoundLight:
    """
    Contrôle le son et les LEDs du robot EV3.
    """

    def __init__(self):
        self.ev3 = EV3Brick()

    def beep(self):
        self.ev3.speaker.beep()

    def play_tone(self, frequency, duration):
        self.ev3.speaker.play_tone(frequency, duration)

    def set_leds(self, color=Color.GREEN):
        self.ev3.light.on(color)

    def flash_leds(self, color=Color.RED, times=3, interval=200):
        for _ in range(times):
            self.ev3.light.on(color)
            self.ev3.wait(interval)
            self.ev3.light.off()
            self.ev3.wait(interval)