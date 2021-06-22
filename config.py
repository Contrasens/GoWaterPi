import Adafruit_DHT
from datetime import datetime

# Which board pin is the automatic pump control connected to?
PUMP_AUTO_PIN = 4

# Which board pin is the manual pump control connected to?
PUMP_MANUAL_PIN = 27

# Which board pin is the green LED connected to?
GREEN_LED_PIN = 22

# Which board pin is the yellow LED connected to?
YELLOW_LED_PIN = 23

# Which board pin is the switch for the manual mode connected to?
SWITCH_MANUAL_PIN = 17

# Which board pin is connected to the internal temperature sensor?
TEMPERATURE_PIN = 25

# Which board pin is connected to the external temperature sensor?
TEMPERATURE_EXT_PIN = 14

# Which board pin is connected to the soil humidity sensor 1?
SOIL_SENSOR1_PIN = 18

# Which board pin is connected to the soil humidity sensor 2?
SOIL_SENSOR2_PIN = 24

# Is the pump plugged into the normally-on socket?
PUMP_DEFAULT_ON = False

# How long should the pump run when engaged (in seconds)?
# 400s --> ca. 9.8 liters
# 300s --> ca. 7.9 liters
# 200s --> ca. 5.4 liters
PUMP_TIME = 100



# Which IP should be used by the web-server?
SERVER_IP = '192.168.0.214'

# Which port should be used by the web-server?
PORT = 8080



# Should I send email notifications?
EMAIL_ACTIVE = True

# Which address(es) to send emails to?
EMAIL_TO_ADDRESS = 'dinu.sarbu@gmail.com'

# Which subject should I use after watering the plants?
EMAIL_SUBJECT_AFTER_WATERING = '[GoWaterPi] Irrigation successful!'

# Which body should I use after watering the plants?
hum_int, temp_int = Adafruit_DHT.read_retry(11, TEMPERATURE_PIN)
hum_ext, temp_ext = Adafruit_DHT.read_retry(11, TEMPERATURE_EXT_PIN)
EMAIL_BODY_TEXT = ('Hi,' + '\n\n' + 
                   'your plants were irrigated for ' + str(PUMP_TIME) + ' seconds.' + '\n\n')
EMAIL_BODY_DATA = ('Date and time:'  + str(datetime.now()) + '\n' + 
                   'Internal temperature: ' + str(temp_int) + '*C, internal humidity: ' + str(hum_int) + '%\n' +
                   'External temperature: ' + str(temp_ext) + '*C, external humidity: ' + str(hum_ext) + '%\n\n')
EMAIL_BODY_SIGN = '\GoWaterPi :)'


