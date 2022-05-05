from gpiozero import Button
import abc

class IButton(metaclass=abc.ABCMeta):
    """
    Defines an interface for some input control.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'change_state') and
                callable(subclass.change_state) and
                hasattr(subclass, 'state_changed') and
                callable(subclass.state_changed) and 
                hasattr(subclass, 'change_permitted') and
                callable(subclass.change_permitted))

    @abc.abstractmethod
    def change_state(self) -> None:
        """First checks change_permitted() and changes state if allowed"""
        raise NotImplementedError

    @abc.abstractmethod
    def state_changed(self) -> bool:
        """Is the current state different from previous state? 
           Side-effect: Updates previous state"""
        raise NotImplementedError

    @abc.abstractmethod
    def change_permitted(self) -> bool:
        """Can state be changed? Should just reference an attribute"""
        raise NotImplementedError

class CherrySwitch(IButton):
    """Standard MX switch but should work w/ any basic button.
        Could be extended to handle an RGB MX switch"""
    def __init__(self, pin:int) -> None:
        """I guess for now assume we are on a Pi"""
        self.pin = pin
        self._state = False
        self._previous_state = True # So that we trigger a change the first time
        self._can_change = True # So that we trigger a change the first time
        self._button = Button(pin) # The underlying gpiozero.Button object

    def change_state(self) -> None:
        if self.change_permitted():
            self._previous_state, self._state = self._state, not self._state
        return None
    
    def state_changed(self) -> bool:
        return self._state == self._previous_state
    
    def change_permitted(self) -> bool:
        """I guess always allow it for now"""
        return True 

