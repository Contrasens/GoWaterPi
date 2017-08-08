import RPi.GPIO as GPIO
import time
import datetime

from flask import Flask, render_template, request
app = Flask(__name__)

from config import (PUMP_AUTO_PIN, PUMP_MANUAL_PIN,
                    GREEN_LED_PIN, YELLOW_LED_PIN,
                    SWITCH_MANUAL_PIN)

GPIO.setmode(GPIO.BCM)  # Numbers GPIOs by physical location

ledGreenStatus = GPIO.LOW
ledYellowStatus = GPIO.HIGH

pins = {
    PUMP_AUTO_PIN: {'name': 'PUMP_AUTO_PIN', 'state': ledYellowStatus},
    PUMP_MANUAL_PIN: {'name': 'PUMP_MANUAL_PIN', 'state': GPIO.LOW},
    GREEN_LED_PIN: {'name': 'GREEN_LED_PIN', 'state': ledGreenStatus},
    YELLOW_LED_PIN: {'name': 'YELLOW_LED_PIN', 'state': ledYellowStatus}
}

# Create a dictionary called switches to store the switches pin number, name,
# pull-up or pull-down and switch position:
switches = {
    SWITCH_MANUAL_PIN: {'name': 'SWITCH_MANUAL_PIN', 'pull_up_down': GPIO.PUD_UP, 'position': 'Automatic'}
}

# Create a dictionary called pins to store the pin number, name, and pin state:
# Set each pin:
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, pins[pin]['state'])

# Set each switch
for switch in switches:
    GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#def setup():
    # GPIO.setup(PUMP_AUTO_PIN, GPIO.OUT, initial=ledYellowStatus)  # Set LedPin's mode is output
    # GPIO.setup(PUMP_MANUAL_PIN, GPIO.OUT, initial=GPIO.LOW)
    # GPIO.setup(GREEN_LED_PIN, GPIO.OUT, initial=ledGreenStatus)  # Set LedPin's mode is output
    # GPIO.setup(YELLOW_LED_PIN, GPIO.OUT, initial=ledYellowStatus)  # Set LedPin's mode is output

    # # Set switches mode to input, and Raspberry Pi's internal pull-up resistors to high level(3.3V)
    # GPIO.setup(SWITCH_MANUAL_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # #GPIO.setup(SWITCH_AUTO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# callback function to service the interrupt
def isrSwitch(ev=None):
    global ledGreenStatus
    global ledYellowStatus
    ledGreenStatus = not ledGreenStatus
    ledYellowStatus = not ledYellowStatus
    if ledGreenStatus:
        setManual()  # set the pump in manual mode
    if ledYellowStatus:
        setAuto()  # set the pump in automatic mode
    setLeds()


# turn on the relay for manual mode
def setManual():
    print(str(datetime.datetime.now()), "Switch set to ""Manual")
    GPIO.output(PUMP_AUTO_PIN, GPIO.HIGH)
    GPIO.output(PUMP_MANUAL_PIN, GPIO.LOW)


# turn on the relay for automatic mode
def setAuto():
    print(str(datetime.datetime.now()), "Switch set to ""Auto")
    GPIO.output(PUMP_AUTO_PIN, GPIO.LOW)
    GPIO.output(PUMP_MANUAL_PIN, GPIO.HIGH)


def setLeds():
    global ledGreenStatus
    global ledYellowStatus
    GPIO.output(GREEN_LED_PIN, ledGreenStatus)
    GPIO.output(YELLOW_LED_PIN, ledYellowStatus)


def loop():
    # wait for raising and set bouncetime to prevent the callback function from being called multiple times
    # when the button is pressed
    GPIO.add_event_detect(SWITCH_MANUAL_PIN, GPIO.BOTH, callback=isrSwitch, bouncetime=300)

    while True:
        time.sleep(1)  # Don't do anything for 1 second


def destroy():
    print "Bye!"
    GPIO.cleanup()  # Release resource



@app.route("/")
def main():
    global pins
    # For each pin, read the pin state and store it in the pins dictionary:
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)
    # Put the pin dictionary into the template data dictionary:
    templateData = {
        'pins': pins
    }
    # Pass the template data into the template main.html and return it to the user
    return render_template('main.html', **templateData)


# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
    global pins
    # Convert the pin from the URL into an integer:
    changePin = int(changePin)
    # Get the device name for the pin being changed:
    deviceName = pins[changePin]['name']
    # If the action part of the URL is "on," execute the code indented below:
    if action == "on":
        # Set the pin high:
        GPIO.output(changePin, GPIO.HIGH)
        # Save the status message to be passed into the template:
        message = "Turned " + deviceName + " on."
    if action == "off":
        GPIO.output(changePin, GPIO.LOW)
        message = "Turned " + deviceName + " off."

    # For each pin, read the pin state and store it in the pins dictionary:
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)

    # Along with the pin dictionary, put the message into the template data dictionary:
    templateData = {
        'pins': pins
    }
    return render_template('main.html', **templateData)


# Program start from here
if __name__ == '__main__':
    print "GoWaterPi started. Ctrl + C to interrupt."
    app.run(host='192.168.0.214', port=8080, debug=True)
    #setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
