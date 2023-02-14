import simpleio
import time
import supervisor

class LEDController():
    def __init__(self, clock, sr_data, red_pin, green_pin, blue_pin):
        self.clock = clock
        self.sr_data = sr_data
        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin
        self.brightness = 0.9

        # Reset all LEDs to avoid flickering
        self.reset_LEDs()


    def reset_LEDs(self):
        """
        Turns off all LEDs.
        """
        # Set all color pins to output a logical low
        self.red_pin.value = False
        self.green_pin.value = False
        self.blue_pin.value = False
				
        # Communicate to the shift register to turn off LEDs
        bitval = 0x00
        simpleio.shift_out(data_pin=self.sr_data, clock=self.clock, value=bitval, msb_first=True)


    def turn_on_LED(self, bitval, color="white", duration=1):
        """
        Turns on the LED(s) encoded in the bit value in the desired color.
        """
        # Send the bit values to the shift register
        simpleio.shift_out(data_pin=self.sr_data, clock=self.clock, value=bitval, msb_first=True)

        # Additional clock pulse since the shift register is one clock pulse ahead of the storage register.
        self.sr_data.value = 0
        self.clock.value = True
        self.clock.value = False
				
        # Set the target color pin(s) to output a logical high
        self.turn_on_PWM(duration, color)


    def turn_on_PWM(self, duration, color):
        """
        Implementation of PWM on a selected pin for a specified duration.
        """
        # Calculate how many times out of 100 (1% steps) the pin needs to be high or low.
        n_high = self.brightness * 100
        n_low = (1-self.brightness) * 100

        start_time = supervisor.ticks_ms()

        if color == "white":
            while supervisor.ticks_ms()-start_time <= duration*1000:
                for _ in range(0, n_high):
                    self.red_pin.value = True
                    self.blue_pin.value = True
                    self.green_pin.value = True
                for _ in range(0, n_low):
                    self.red_pin.value = False
                    self.blue_pin.value = False
                    self.green_pin.value = False

        elif color == "green":
            while supervisor.ticks_ms()-start_time <= duration*1000:
                for _ in range(0, n_high):
                    self.green_pin.value = True
                for _ in range(0, n_low):
                    self.green_pin.value = False

        elif color == "red":
            while supervisor.ticks_ms()-start_time <= duration*1000:
                for _ in range(0, n_high):
                    self.red_pin.value = True
                for _ in range(0, n_low):
                    self.red_pin.value = False

        elif color == "blue":
            while supervisor.ticks_ms()-start_time <= duration*1000:
                for _ in range(0, n_high):
                    self.blue_pin.value = True
                for _ in range(0, n_low):
                    self.blue_pin.value = False


    def blink_LED(self, bitval=0xFF, color="white", times=10, interval=0.33):
        """
        Turns the LEDs (as indicated by the bitval) on and off for a defined amount of
        times. The default settings are 10 blinks with an interval of 0.33 ms in white.
        """
        for _ in range(0, times):
            self.turn_on_LED(bitval, color=color, duration=interval)
            time.sleep(interval)


    def show_battery_status(self, battery_status):
        """
        Indicates the battery status with a visual bar, where the lowest row corresponds
        to an empty battery and the highest corresponds to a full battery.
        """
        # Define the order in which the LED rows should be turned on
        row_order = [0x88, 0xCC, 0xEE, 0xFF]

        # Show the battery status with a visual bar
        for idx in range(0, battery_status):
            self.turn_on_LED(bitval=row_order[idx], duration=0.5)

        time.sleep(0.75)

        # Give visual feedback whether the battery is full enough (green blinking) or not (red blinking)
        if battery_status > 1:
            self.blink_LED(bitval=row_order[battery_status-1], interval=0.2, times=3, color="green")
        else:
            self.blink_LED(bitval=row_order[battery_status-1], interval=0.2, times=3, color="red")


    def indicate_low_battery(self):
        """
        Blinks in red to indicate low battery.
        """
        while True:
            self.blink_LED(color="red")


    def modulate_brightness(self, brightness):
        """
        Modulates the brightness. The brightness should be
        a value between 0 (0%) and 1 (100%), where 1 corresponds to the maximal brightness.
        """
        # Round brightness to 0.01 decimals (100 brightness levels)
        self.brightness = (round(brightness * 100) / 100)
