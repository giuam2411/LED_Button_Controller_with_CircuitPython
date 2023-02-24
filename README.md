# LED_Button_Controller_with_CircuitPython

Code for a Arduino Seeeduino XIAO Microcontroller used in a University competition. 

## Description 
The board used in this competition consists of a Arduino Seeeduino XIAO Microcontroller connected to eight push buttons and eight LEDs over a shift register (SN74HCS596). One of the push buttons is set as the target button. The code detects button presses by a user. If a button was pressed, the user receives visual feedback in the form of green (if the target button was pressed) or red (if another button was pressed) light. The Flowchart below describes the logic of the application.  

![Flowchart](Flowchart.jpg)

## How to get started
To test the code, install and run CircuitPython by Adafruit Industries on your Arduino Seeduino XIAO. 

### CircuitPython for Low-Costs Microcontrollers
CircuitPython is a programming language that was created to simplify programming on low-cost microcontroller boards. As no desktop downloads are required, getting started is faster than ever. After you've set up your board, you can install this code and review it on any test editor. Please see here for further information on CircuitPython: https://circuitpython.org/. 

### Installing CircuitPython
To use CircuitPython on your Seeduino XIAO, download the official CircuitPython Bootloader here: https://circuitpython.org/board/seeeduino_xiao/. 
Then, connect the Seeed Studio XIAO SAMD21 to your PC via USB Type-C. Use a jumper to short connect RST Pins twice to access the DFU bootloader mode. 
In your PC, an external drive named Arduino should appear. Transfer the CircuitPython uf2 files you downloaded to the Arduino drive. Unplug and reconnect the USB Type-C after loading the CircuitPython Bootloader. CIRCUITPY, a new external drive, should appear. CircuitPython is now installed on the Seeeduino. Now, simply clone the code and libraries from this repository, and drag them onto the CIRCUITPY disk. That's it: Your board is ready to use! 

For more information on how to install CircuitPython on your board, and for CircuitPython basics, please see https://wiki.seeedstudio.com/Seeeduino-XIAO-CircuitPython/.
