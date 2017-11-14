import RPi.GPIO as GPIO
import config


# the function to print values out
def print_out_value(channel):
    sensor = 1
    if channel == channel2:
	sensor = 2

    if get_moisture(channel):
        print "Sensor%d off - soil is dry" % sensor
    else:
        print "Sensor%d on  - soil is wet" % sensor

# return value of the soil sensor:
# True - soil is wet
# False - soil is dry
def get_moisture(channel):
    return GPIO.input(channel)

# decide if plant needs watering
def needs_water():
    if get_moisture(channel1) and get_moisture(channel2):
        return False
    else:
        return True

# set channels
channel1 = config.SOIL_SENSOR1_PIN
channel2 = config.SOIL_SENSOR2_PIN

# set GPIO numbering to BCM
GPIO.setmode(GPIO.BCM)

# set the pins of the two soil moisture sensors as input
GPIO.setup(channel1, GPIO.IN)
GPIO.setup(channel2, GPIO.IN)

# read values
value1 = GPIO.input(channel1)
value2 = GPIO.input(channel2)

# print values
print_out_value(channel1)
print_out_value(channel2)

