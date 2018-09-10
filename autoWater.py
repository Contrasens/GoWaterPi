import RPi.GPIO as GPIO
import time
import datetime
import config


def setup():
    GPIO.setmode(GPIO.BCM)  # Numbers GPIOs by physical location
    GPIO.setwarnings(False)

    # Pump pins
    GPIO.setup(config.PUMP_AUTO_PIN, GPIO.OUT, initial=GPIO.HIGH)

    # LEDs
    GPIO.setup(config.YELLOW_LED_PIN, GPIO.OUT, initial=GPIO.LOW)  # Set LedPin's mode is output

    # Sensors
    GPIO.setup(config.SOIL_SENSOR1_PIN, GPIO.IN)
    GPIO.setup(config.SOIL_SENSOR2_PIN, GPIO.IN)

def startPump():
    print(str(datetime.datetime.now()), "autoWater started for ", config.PUMP_TIME, ' seconds.')
    GPIO.output(config.YELLOW_LED_PIN, GPIO.HIGH)
    GPIO.output(config.PUMP_AUTO_PIN, GPIO.LOW)


def stopPump():
    GPIO.output(config.YELLOW_LED_PIN, GPIO.LOW)
    GPIO.output(config.PUMP_AUTO_PIN, GPIO.HIGH)
    print(str(datetime.datetime.now()), "autoWater finished.")
    GPIO.cleanup()  # Release resource


def destroy():
    print ('Bye!')
    GPIO.cleanup()  # Release resource


if __name__ == '__main__':  # Program start from here
    setup()

    try:
        startPump()
        time.sleep(config.PUMP_TIME)  # Don't do anything for predefined amount of seconds
        stopPump()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
