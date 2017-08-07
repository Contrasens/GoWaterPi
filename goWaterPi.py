import RPi.GPIO as GPIO
import time
import datetime
from config import (PUMP_AUTO_PIN, PUMP_MANUAL_PIN,
                    GREEN_LED_PIN, YELLOW_LED_PIN,
                    SWITCH_MANUAL_PIN)

ledGreenStatus = GPIO.LOW
ledYellowStatus = GPIO.HIGH


def setup():
    GPIO.setmode(GPIO.BCM)  # Numbers GPIOs by physical location

    GPIO.setup(PUMP_AUTO_PIN, GPIO.OUT, initial=ledYellowStatus)  # Set LedPin's mode is output
    GPIO.setup(PUMP_MANUAL_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(GREEN_LED_PIN, GPIO.OUT, initial=ledGreenStatus)  # Set LedPin's mode is output
    GPIO.setup(YELLOW_LED_PIN, GPIO.OUT, initial=ledYellowStatus)  # Set LedPin's mode is output

    # Set switches mode to input, and Raspberry Pi's internal pull-up resistors to high level(3.3V)
    GPIO.setup(SWITCH_MANUAL_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #GPIO.setup(SWITCH_AUTO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


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


if __name__ == '__main__':  # Program start from here
    print "GoWaterPi started. Ctrl + C to interrupt."
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
