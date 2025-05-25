import smtplib
from email.mime.text import MIMEText
import config
import Adafruit_DHT as DHT11
import RPi.GPIO as GPIO

# --- Email configuration ---
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'your_email@gmail.com'
EMAIL_PASSWORD = 'your_app_password'  # Use an app password if using Gmail 2FA
TO_EMAIL = 'recipient_email@example.com'
# ---------------------------

print("Preparing request...")

# Set GPIO numbering to BCM
GPIO.setmode(GPIO.BCM)

# Get temperature and humidity from the external and internal sensors
duration = config.PUMP_TIME
e_hum, e_temp = DHT11.read_retry(11, config.TEMPERATURE_EXT_PIN)
i_hum, i_temp = DHT11.read_retry(11, config.TEMPERATURE_PIN)

# Set soil sensors as input and get soil humidity
channel_1 = config.SOIL_SENSOR1_PIN
channel_2 = config.SOIL_SENSOR2_PIN
GPIO.setup(channel_1, GPIO.IN)
GPIO.setup(channel_2, GPIO.IN)

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

soil1_str = get_soil_humidity(channel_1)
soil2_str = get_soil_humidity(channel_2)

# Set environment strings
env_ext = "  <b>Outside</b>: " + str(e_temp) + "°C | " + str(e_hum) + "%"
env_int = "  <b>Inside the box</b>: " + str(i_temp) + "°C | " + str(i_hum) + "%"

# Prepare strings for the email body
soil_details = soil1_str + "<br>" + soil2_str
env_details = env_ext + "<br>" + env_int

subject = f"Watering System Alert: {duration} seconds"
body = f"""
<html>
<body>
<h2>Watering System Report</h2>
<p><b>Pump Duration:</b> {duration} seconds</p>
<p>{env_details}</p>
<p>{soil_details}</p>
</body>
</html>
"""

msg = MIMEText(body, 'html')
msg['Subject'] = subject
msg['From'] = EMAIL_ADDRESS
msg['To'] = TO_EMAIL

try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
    print("Email sent successfully!")
except Exception as e:
    print("Failed to send email:", e)

print("Done!")
