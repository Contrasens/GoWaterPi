import requests
import config
import Adafruit_DHT as DHT11


print ("Preparing request...")

def email_alert(first, second, third):
	report = {}
	report["value1"] = first
	report["value2"] = second
	report["value3"] = third
	requests.post('https://maker.ifttt.com/trigger/<YOUR_EVENT_NAME>/with/key/<YOUR_API_KEY>', data=report)
	print ("Request: ", report)

duration = config.PUMP_TIME
e_hum, e_temp = DHT11.read_retry(11, config.TEMPERATURE_EXT_PIN)
i_hum, i_temp = DHT11.read_retry(11, config.TEMPERATURE_PIN)

external = str(e_temp) + "°C, " + str(e_hum) + "%"
internal = str(i_temp) + "°C, " + str(i_hum) + "%"

email_alert(duration, external, internal)

print ("Done!")
