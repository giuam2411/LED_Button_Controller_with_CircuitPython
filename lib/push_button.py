import supervisor
import board
from analogio import AnalogIn


class PushButton:
    def __init__(self, pin, target_voltage, name, back_light):
        self.pin = pin
        self.target_voltage = target_voltage
        self.last_button_state = False
        self.last_debounce_time = 0
        self.threshold = 0.1  # V
        self.debounce_delay = 5  # ms
        self.is_target_button = False
        self.name = name
        self.back_light = back_light


    def get_voltage(self):
        """
        Takes a pin and returns its analogue input value in V.
        """
        return (self.pin.value * 3.3) / 65536


    def get_button_state(self):
        """
        This function takes the pin voltage and returns the
        button state, where "pressed" = True and "not pressed" = False.
        """
        if abs(self.get_voltage() - self.target_voltage) < self.threshold:
            button_state = True
        else:
            button_state = False

        return button_state


    def get_debounced_signal(self):
        """
        Takes the current reading of the push button, debounces the signal based
        on the previous button states and returns whether the button has been pressed.
        """
        button_pressed = False
        current_button_state = self.get_button_state()

        # Check if the switch changed, due to noise or pressing
        if current_button_state != self.last_button_state:
            # Reset the debouncing timer
            self.last_debounce_time = supervisor.ticks_ms()

        # Check if the reading has been constant for longer than the debounce delay
        if (supervisor.ticks_ms() - self.last_debounce_time) > self.debounce_delay:

            # Return if the button was pressed
            if current_button_state:
                button_pressed = True

        self.last_button_state = current_button_state

        return button_pressed
