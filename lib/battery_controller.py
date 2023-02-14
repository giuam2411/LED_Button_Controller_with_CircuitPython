class BatteryController():
    def __init__(self, pin, max_voltage):
        self.pin = pin
        self.max_voltage = max_voltage

    def get_battery_voltage(self):
        """
        Takes a pin and returns its analogue input value in V.
        """
        return (self.pin.value * 3.3) / 65536

    def get_battery_status(self):
        """
        Takes the current battery voltage and returns a categorical value (0, 1, 2, 3 or 4),
        where 0 corresponds to an empty battery and 4 corresponds to a full battery.
        """
        # Set the bin boundaries and the corresponding status descriptions.
        bins = [0, self.max_voltage*1/4, self.max_voltage*2/4, self.max_voltage*3/4, self.max_voltage]
        status = [0, 1, 2, 3, 4]

        # Categorize the current battery voltage
        for idx, boundary in enumerate(bins):
            if (round(self.get_battery_voltage(),3) <= round(boundary,3)):
                return int(status[idx])
