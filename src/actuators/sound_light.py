"""
Module to control the EV3 brick's audio and visual feedback features.
Provides a unified interface for controlling the speaker and LEDs.
"""

from pybricks.hubs import EV3Brick
from pybricks.parameters import Color
from pybricks.tools import wait

class SoundLight:
    """
    Contrôle le son et les LEDs du robot EV3.
    """

    def __init__(self):
        self.ev3 = EV3Brick()

    def beep(self):
        """
        Plays a single beep sound using the EV3's speaker.
        """
        self.ev3.speaker.beep()

    def play_tone(self, frequency, duration):
        """
        Plays a tone at a specified frequency and duration.

        Args:
            frequency (int): The frequency of the tone in Hz
            duration (int): The duration of the tone in milliseconds
        """
        self.ev3.speaker.beep(frequency=frequency, duration=duration)

    def set_leds(self, color=Color.GREEN):
        """
        Sets the EV3's LED color.

        Args:
            color (Color): The color to set the LED to, defaults to green
        """
        self.ev3.light.on(color)

    def flash_leds(self, color=Color.RED, times=3, interval=200):
        """
        Flashes the EV3's LED in a pattern.

        Args:
            color (Color): The color to flash, defaults to red
            times (int): Number of times to flash, defaults to 3
            interval (int): Time between flashes in milliseconds, defaults to 200
        """
        for _ in range(times):
            self.ev3.light.on(color)
            wait(interval)
            self.ev3.light.off()
            wait(interval)
