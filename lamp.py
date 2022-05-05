import abc
import random
from typing import Tuple
import RPi.GPIO as GPIO

class ILamp(metaclass=abc.ABCMeta):
    """
    Defines an interface for lamp objects.
    The type of lamp object can be a Neopixel, RGB LED, or whatever,
    provided it implements the following methods
    """
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'set_color') and
                callable(subclass.set_color) and
                hasattr(subclass, 'get_color') and
                callable(subclass.get_color) and
                hasattr(subclass, 'set_brightness') and
                callable(subclass.set_brightness) and
                hasattr(subclass, 'get_brightness') and
                callable(subclass.get_brightness) and
                hasattr(subclass, 'set_state') and
                callable(subclass.set_state) and
                hasattr(subclass, 'get_state') and
                callable(subclass.get_state) and
                hasattr(subclass, 'flash') and
                callable(subclass.flash) and
                hasattr(subclass, 'pulsate') and
                callable(subclass.pulsate))

    @abc.abstractmethod
    def set_color(self, rgb: Tuple[int, int, int]) -> None:
        """Sets the lamp to a specific (red, green, blue) color value"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_color(self) -> Tuple[int, int, int]:
        """Returns the current color value as (red, green, blue)"""
        raise NotImplementedError

    @abc.abstractmethod
    def set_brightness(self, brightness: float) -> None:
        """Sets brightness between 0.0 and 1.0 where 1.0 is full
            brightness"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_brightness(self) -> float:
        """Returns current brightness between 0.0 and 1.0"""
        raise NotImplementedError

    @abc.abstractmethod
    def set_state(self, state: bool) -> None:
        """Turns on the lamp"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_state(self) -> bool:
        """Turns off the lamp"""
        raise NotImplementedError

    @abc.abstractmethod
    def flash(self, n_flashes: int) -> None:
        """Turns the lamp on and off 'n_flashes' number of times"""
        raise NotImplementedError

    @abc.abstractmethod
    def pulsate(self, n_pulsations: int, n_seconds: int) -> None:
        """
        Decreases brightness and increases back to original level over
          `n_seconds`. Repeats this `n_pulsations` times
        """
        raise NotImplementedError


def validate_color(rgb: Tuple[int, int, int]) -> bool:
    """Checks if colors are in bounds"""
    for i, val in enumerate(rgb):
        if val < 0 or val > 255:
            piece = 'RGB'[i]
            return False
    return True


def validate_brightness(brightness: float) -> bool:
    """Checks if brightness is in bound"""
    if brightness < 0.0 or brightness > 1.0:
        return False
    return True


def suggest_rgb(current: Tuple[int, int, int]) -> Tuple[int, int, int]:
    """
    Returns a random rgb tuple from Adafruit's pallette:
    https://docs.circuitpython.org/projects/led-animation/en/latest/api.html#adafruit-led-animation-color
    """
    colors = [
        (255, 100, 0), # Amber
        (50, 255, 255), # Aqua
        (255, 255, 255), # White
        (0, 0, 255), # Blue
        (0, 255, 255), # Cyan
        (255, 222, 30), # Gold
        (0, 255, 0), # Green
        (0, 255, 40), # Jade
        (255, 0, 20), # Magenta
        (253, 245, 230), # Old Lace
        (255, 40, 0), # Orange
        (242, 90, 255), # Pink
        (180, 0, 255) # Purple
    ]
    return random.choice([color for color in colors if color != current])


def rgb_encode(rgb: Tuple[int, int, int]) -> int:
    red, green, blue = rgb
    encoded_rgb = red
    encoded_rgb = (encoded_rgb << 8) + green
    encoded_rgb = (encoded_rgb << 8) + blue
    return encoded_rgb


def rgb_decode(encoded_rgb: int) -> Tuple[int, int, int]:
    red = (encoded_rgb >> 16) & 0xff
    green = (encoded_rgb >> 8) & 0xff
    blue = encoded_rgb & 0xff
    return (red, green, blue)


class WS2812B(ILamp):
    """
    Will write this when I have the hardware.
    Details here: 
      https://learn.sparkfun.com/tutorials/ws2812-breakout-hookup-guide;
    """
    pass


class Console(ILamp):
    """
    A version for dev / debug purposes. Prints information out to the
    console. 
    """

    def __init__(self, rgb: Tuple[int, int, int] = (0, 0, 0),
                 brightness: float = 1.0, state: bool = True):
        if not validate_color(rgb):
            raise Exception(f'Each color must be in range 0:255')
        self.rgb = rgb
        if not validate_brightness(brightness):
            raise Exception(f'Brightness must but in range 0.0:1.0')
        self.brightness = brightness
        print(f'Created Console Lamp with color {self.rgb} and brightness {self.brightness}')
        self.state = state
        if self.state:
            print('Lamp is currently on')
        else:
            print('Lamp is currently off')

    def set_color(self, rgb: Tuple[int, int, int]) -> None:
        if not validate_color(rgb):
            raise Exception(f'Each color must be in range 0:255')
        self.rgb = rgb
        print(f'Color now set to {self.rgb}')
        return None
    
    def get_color(self) -> Tuple[int, int, int]:
        print(f'Current color: {self.rgb}')
        return self.rgb
    
    def set_brightness(self, brightness: float) -> None:
        if not validate_brightness(brightness):
            raise Exception(f'Brightness must but in range 0.0:1.0')
        self.brightness = brightness
        print(f'Brightness now {self.brightness}')
        return None
    
    def get_brightness(self) -> float:
        print(f'Current brightness: {self.brightness}')
        return self.brightness
    
    def set_state(self, state: bool) -> None:
        self.state = state
        if self.state:
            print('Lamp is currently on')
        else:
            print('Lamp is currently off')
        return None
    
    def get_state(self) -> bool:
        if self.state:
            print('Lamp is currently on')
        else:
            print('Lamp is currently off')
        return self.state

    def flash(self, n_flashes: int) -> None:
        print(f'Now flashing {n_flashes} times:')
        if not self.get_state:
            self.set_state(True)
        for i in range(n_flashes):
            print(f'--> Flash {i}')
            self.set_state(False)
            self.set_state(True)
        print(f'Done flashing')
        return None
    
    def pulsate(self, n_pulsations: int, n_seconds: int) -> None:
        import time
        print(f'Starting {n_pulsations} pulsations with a period of {n_seconds}')
        for i in range(n_pulsations):
            print(f'--> Pulsation {i} start')
            time.sleep(n_seconds)
            print(f'--> Pulsation {i} finish')
        print(f'Finished pulsations')
        return None


def main():
    test_lamp = Console((1,2,3), 0.5)
    test_lamp.flash(5)


if __name__ == '__main__':
    main()
