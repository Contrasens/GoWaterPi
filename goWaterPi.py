import RPi.GPIO as GPIO
import time
import datetime

pinGreen = 22  # Manual mode
pinYellow = 23  # Automatic mode

switchMan = 17  # switch in MANUAL mode (when switch in this position, water pump goes on)
switchAuto = 18  # switch in AUTO mode (pumping water only on schedule, sensor-based etc.)

ledGreenStatus = 0
ledYellowStatus = 1


def setup():
    GPIO.setmode(GPIO.BCM)  # Numbers GPIOs by physical location

    GPIO.setup(pinGreen, GPIO.OUT, initial=ledGreenStatus)  # Set LedPin's mode is output
    GPIO.setup(pinYellow, GPIO.OUT, initial=ledYellowStatus)  # Set LedPin's mode is output

    # Set switchON_OFF's mode is input, and pull up to high level(5V)
    GPIO.setup(switchMan, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(switchAuto, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def swManAuto(ev=None):
    print(str(datetime.datetime.now()), " Switch GREEN and YELLOW")
    global ledGreenStatus
    global ledYellowStatus
    ledGreenStatus = not ledGreenStatus
    ledYellowStatus = not ledYellowStatus
    setLeds()


def setLeds():
    global ledGreenStatus
    global ledYellowStatus
    GPIO.output(pinGreen, ledGreenStatus)
    GPIO.output(pinYellow, ledYellowStatus)


def loop():
    # wait for raising and set bouncetime to prevent the callback function from being called multiple times when the button is pressed
    GPIO.add_event_detect(switchMan, GPIO.BOTH, callback=swManAuto, bouncetime=300)

    while True:
        time.sleep(1)  # Don't do anything


def destroy():
    # GPIO.output(pinRed, GPIO.LOW)    # led off
    # GPIO.output(pinGreen, GPIO.LOW)    # led off
    GPIO.cleanup()  # Release resource


if __name__ == '__main__':  # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
