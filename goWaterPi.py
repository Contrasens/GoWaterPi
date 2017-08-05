import RPi.GPIO as GPIO
import time, datetime

pinRed      = 27    # System ON
pinGreen    = 22    # Manual mode
pinYellow   = 23    # Automatic mode

switchON_OFF = 25

switchMan   = 17
switchAuto  = 18

ledRedStatus    = 1
ledGreenStatus  = 0
ledYellowStatus = 1

def setup():
    GPIO.setmode(GPIO.BCM)          # Numbers GPIOs by physical location
    
    GPIO.setup(pinRed,    GPIO.OUT, initial = ledRedStatus) # Set LedPin's mode is output
    GPIO.setup(pinGreen,  GPIO.OUT, initial = ledGreenStatus) # Set LedPin's mode is output
    GPIO.setup(pinYellow, GPIO.OUT, initial = ledYellowStatus) # Set LedPin's mode is output

    GPIO.setup(switchON_OFF, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set switchON_OFF's mode is input, and pull up to high level(5V)
    GPIO.setup(switchMan,    GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set switchON_OFF's mode is input, and pull up to high level(5V)
    GPIO.setup(switchAuto,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set switchOFF's mode is input, and pull up to low level(0V)

def swLedRed(ev=None):
    print(str(datetime.datetime.now()), " Switch RED")
    global ledRedStatus
    ledRedStatus = not ledRedStatus
    setLeds()

def swManAuto(ev=None):
    print(str(datetime.datetime.now()), " Switch GREEN and YELLOW")
    global ledRedStatus
    global ledGreenStatus
    global ledYellowStatus
    if (ledRedStatus):
        ledGreenStatus = not ledGreenStatus
        ledYellowStatus = not ledYellowStatus
        setLeds()
    else:
        ledGreenStatus = 0
        ledYellowStatus = 0
        setLeds()

def setLeds():
    global ledRedStatus
    global ledGreenStatus
    global ledYellowStatus
    GPIO.output(pinRed,    ledRedStatus)  
    GPIO.output(pinGreen,  ledGreenStatus)  
    GPIO.output(pinYellow, ledYellowStatus)
            
    
def loop():
     # wait for raising and set bouncetime to prevent the callback function from being called multiple times when the button is pressed
    GPIO.add_event_detect(switchON_OFF, GPIO.RISING, callback=swLedRed, bouncetime=500)
    GPIO.add_event_detect(switchMan,    GPIO.RISING, callback=swManAuto, bouncetime=500)
    #GPIO.add_event_detect(switchAuto,   GPIO.RISING, callback=swManAuto, bouncetime=1000)

    while True:
        time.sleep(1)   # Don't do anything

def destroy():
    #GPIO.output(pinRed, GPIO.LOW)    # led off
    #GPIO.output(pinGreen, GPIO.LOW)    # led off
    GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()


