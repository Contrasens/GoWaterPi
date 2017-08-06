import RPi.GPIO as GPIO
import time
import datetime

pinAuto = 4  # Controls the relay that triggers manually the water pump
pinManual = 27  # Controls the relay that triggers automatically the water pump
pinGreen = 22  # Manual mode
pinYellow = 23  # Automatic mode

switchMan = 17  # switch in MANUAL mode (when switch in this position, water pump goes on)
switchAuto = 18  # switch in AUTO mode (pumping water only on schedule, sensor-based etc.)

ledGreenStatus = GPIO.LOW
ledYellowStatus = GPIO.HIGH


def setup():
    GPIO.setmode(GPIO.BCM)  # Numbers GPIOs by physical location

    GPIO.setup(pinAuto, GPIO.OUT, initial=ledYellowStatus)  # Set LedPin's mode is output
    GPIO.setup(pinManual, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(pinGreen, GPIO.OUT, initial=ledGreenStatus)  # Set LedPin's mode is output
    GPIO.setup(pinYellow, GPIO.OUT, initial=ledYellowStatus)  # Set LedPin's mode is output

    # Set switches mode to input, and Raspberry Pi's internal pull-up resistors to high level(3.3V)
    GPIO.setup(switchMan, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(switchAuto, GPIO.IN, pull_up_down=GPIO.PUD_UP)


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
    GPIO.output(pinAuto, GPIO.HIGH)
    GPIO.output(pinManual, GPIO.LOW)


# turn on the relay for automatic mode
def setAuto():
    print(str(datetime.datetime.now()), "Switch set to ""Auto")
    GPIO.output(pinAuto, GPIO.LOW)
    GPIO.output(pinManual, GPIO.HIGH)


def setLeds():
    global ledGreenStatus
    global ledYellowStatus
    GPIO.output(pinGreen, ledGreenStatus)
    GPIO.output(pinYellow, ledYellowStatus)


def loop():
    # wait for raising and set bouncetime to prevent the callback function from being called multiple times
    # when the button is pressed
    GPIO.add_event_detect(switchMan, GPIO.RISING, callback=isrSwitch, bouncetime=200)

    while True:
        time.sleep(1)  # Don't do anything for 1 second


def destroy():
    print "Bye!"
    GPIO.cleanup()  # Release resource


if __name__ == '__main__':  # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
