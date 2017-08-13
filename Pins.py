import RPi.GPIO as GPIO
from threading import Timer
import config


def init():
    GPIO.setwarnings(False)  # suppress GPIO used message
    GPIO.setmode(GPIO.BCM)  # use BCM pin numbers
    GPIO.setup(config.YELLOW_LED_PIN, GPIO.OUT)  # set LED pin as output
    GPIO.setup(config.GREEN_LED_PIN, GPIO.OUT)  # set LED pin as output
    GPIO.setup(config.PUMP_AUTO_PIN, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(config.PUMP_MANUAL_PIN, GPIO.OUT, initial=GPIO.HIGH)

    # set switch pin as input
    # also use internal pull-up so we don't need external resistor
    GPIO.setup(config.SWITCH_MANUAL_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def ledOn(pin):
    GPIO.output(pin, GPIO.HIGH)

def ledOff(pin):
    GPIO.output(pin, GPIO.LOW)


def setLED(state):
    if state:
        ledOn()
    else:
        ledOff()


def setPump(pin, state):
    if state:
        GPIO.output(pin, GPIO.HIGH)
    else:
        GPIO.output(pin, GPIO.LOW)



# the "not" is used to reverse the state of the input
# when pull-up is used, 1 is returned when the switch is not pressed
def readState():
    if not GPIO.input(config.SWITCH_MANUAL_PIN):
        return True  # Manual On
    else:
        return False  # Manual Off


# read the pump state (On / Off)
def readPump(pin):
    if GPIO.input(pin):
        return True
    else:
        return False

# stops the pump
def stopPump(pin):
    if GPIO.output(pin, GPIO.HIGH):
        GPIO.output(pin, GPIO.LOW)


# countdown - after a time period, a function is called
def countdown(periodSeconds):
    t = Timer(float(periodSeconds), stopPump)
    t.start()  # after 30 seconds, "hello, world" will be printed


# if not used as a module (standalone), run this test program
if __name__ == "__main__":
    init()
    try:
        while True:
            setLED(readState())
    except:
        # clean exit on CTRL-C
        GPIO.cleanup()
        quit()
