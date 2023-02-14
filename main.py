# Load libraries
import time
import board
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn
from push_button import PushButton
from led_controller_with_PWM import LEDController
from battery_controller import BatteryController


#--------------------------------------------------------------------
# Define variables

TARGET_V1 = 2.63 #V
TARGET_V2 = 2.27 #V
MAX_VBAT = 2.6 #V --> TODO: Check with Michi


#-------------------------------------------------------------------
# Set up

# Set up analog inputs
analog_in_1_7 = AnalogIn(board.A6)
analog_in_2_8 = AnalogIn(board.A7)
analog_in_3_5 = AnalogIn(board.A8)
analog_in_4_6 = AnalogIn(board.A9)
analog_vbat = AnalogIn(board.A10)

# Set up buttons
PB_1 = PushButton(pin=analog_in_1_7, target_voltage=TARGET_V1, name="PB_1", back_light=0x01)
PB_2 = PushButton(pin=analog_in_2_8, target_voltage=TARGET_V1, name="PB_2", back_light=0x02)
PB_3 = PushButton(pin=analog_in_3_5, target_voltage=TARGET_V1, name="PB_3", back_light=0x04)
PB_4 = PushButton(pin=analog_in_4_6, target_voltage=TARGET_V1, name="PB_4", back_light=0x08)
PB_5 = PushButton(pin=analog_in_3_5, target_voltage=TARGET_V2, name="PB_5", back_light=0x10)
PB_6 = PushButton(pin=analog_in_4_6, target_voltage=TARGET_V2, name="PB_6", back_light=0x20)
PB_7 = PushButton(pin=analog_in_1_7, target_voltage=TARGET_V2, name="PB_7", back_light=0x40)
PB_8 = PushButton(pin=analog_in_2_8, target_voltage=TARGET_V2, name="PB_8", back_light=0x80)

all_buttons = [PB_1, PB_2, PB_3, PB_4, PB_5, PB_6, PB_7, PB_8]

# Set up clock and data pins for LEDs
sr_data = DigitalInOut(board.D4)
clock = DigitalInOut(board.D5)
sr_data.direction = Direction.OUTPUT
clock.direction = Direction.OUTPUT

# Set up color pins
red_pin = DigitalInOut(board.D0)
green_pin = DigitalInOut(board.D1)
blue_pin = DigitalInOut(board.D2)
red_pin.direction = Direction.OUTPUT
green_pin.direction = Direction.OUTPUT
blue_pin.direction = Direction.OUTPUT

# Set up LED controller
LED_controller = LEDController(clock, sr_data, red_pin, green_pin, blue_pin)

# Set up battery controller
battery = BatteryController(pin=analog_vbat, max_voltage=MAX_VBAT)

#---------------------------------------------------------------------
# Main code

# 0. Check battery status when the device is turned on
battery_status = battery.get_battery_status()
LED_controller.show_battery_status(battery_status)


# 1. Set target button
no_target_button = True
while no_target_button:
    # Iterate through the push buttons until a target button is set
    for button in all_buttons:
        button_pressed = button.get_debounced_signal()
        if button_pressed:
            # If a button is pressed, set it as the target button and give visual feedback
            button.is_target_button = True
            LED_controller.turn_on_LED(bitval=button.back_light, color="blue", duration=1)
            no_target_button = False


# 2. React to button presses
while True:
    # Continuously iterate through the push buttons
    for button in all_buttons:
        button_pressed = button.get_debounced_signal()
        if button_pressed:
            # If a button is pressed, give visual feedback
            if button.is_target_button:
                LED_controller.turn_on_LED(bitval=button.back_light, color="green", duration=2)
            else:
                LED_controller.turn_on_LED(bitval=button.back_light, color="red", duration=2)
            #time.sleep(0.5)

    # Check battery status
    # Get current battery voltage in % of max. battery voltage
    pct_vbat = battery.get_battery_voltage()/MAX_VBAT

    # Modulate the brightness of the LEDs depending on the battery voltage
    if pct_vbat < 0.9:
        LED_controller.modulate_brightness(brightness=current_vbat)

    # Indicate low battery status (<= 1/4 of the maximum voltage)
    if pct_vbat < 0.25:
        LED_controller.indicate_low_battery()


