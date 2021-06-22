import requests
import config
import Adafruit_DHT as DHT11
import RPi.GPIO as GPIO

soil1_str = "N/A"
soil2_str = "N/A"

print ("Preparing request...")

def email_alert(first, second, third):
	report = {}
	report["value1"] = first
	report["value2"] = second
	report["value3"] = third
	requests.post('https://maker.ifttt.com/trigger/WaterON/with/key/6mcriKnzjHjCKnVXGZlzB', data=report)
	print ("Request: ", report)

def get_soil_humidity(channel):
	if channel == channel_1:
		if GPIO.input(channel_1):
			return "<b>Sensor 1</b>: soil is DRY"
		else:
			return "<b>Sensor 1</b>: soil is WET"
	if channel == channel_2:
		if GPIO.input(channel_2):
			return "<b>Sensor 2</b>: soil is DRY"
		else:
			return "<b>Sensor 2</b>: soil is WET"

# set GPIO numberting to BCM
GPIO.setmode(GPIO.BCM)

# get temperature and humidity from the external and internal sensors
duration = config.PUMP_TIME
e_hum, e_temp = DHT11.read_retry(11, config.TEMPERATURE_EXT_PIN)
i_hum, i_temp = DHT11.read_retry(11, config.TEMPERATURE_PIN)

# set soil sensors as input and get soil humidity
channel_1 = config.SOIL_SENSOR1_PIN
channel_2 = config.SOIL_SENSOR2_PIN
GPIO.setup(channel_1, GPIO.IN)
GPIO.setup(channel_2, GPIO.IN)
soil_1 = GPIO.input(channel_1)
soil_2 = GPIO.input(channel_2)
soil1_str = get_soil_humidity(channel_1)
soil2_str = get_soil_humidity(channel_2)

# set environment strings
env_ext = "  <b>Outside</b>: " + str(e_temp) + "°C | " + str(e_hum) + "%"
env_int = "  <b>Inside the box</b>: " + str(i_temp) + "°C | " + str(i_hum) + "%"

# prepare strings for the email body
soil_details = soil1_str + "<br>"  + soil2_str
env_details  = env_ext   + "<br>" + env_int

email_alert(duration, env_details, soil_details)

print ("Done!")
