# GoWaterPi
A plant irigation system based on Raspberry Pi, either manual or at scheduled intervals. A submersible water pump is started to water the plants, then stopped after a configurable time interval.

Currently, the system works in two modes:
1. a Python script is started by a Cron job at predifined intervals (see http://www.adminschoice.com/crontab-quick-reference). The Python script starts the water pump and keeps it running for a time priod which is specified in a configuration file, OR

2. a webpage is available at the Raspis webserver to monitor the activity of the watering system over the internet, and switch it on and off remotely. A web-server must be set up, and the server port must be opened in your router to be able to access it from remote locations. Of course, then a wireless USB dongle is needed, which is able to work from inside the case. The web-page version uses Flask and Ajax, an introduction on how to install them can be found here: http://randomnerdtutorials.com/raspberry-pi-web-server-using-flask-to-control-gpios/

Newest feature:
-----------
Now an email is send to a selected email address when the watering finishes. The email informs about the duration of the watering, time, and internal & external temperature and humidity. Info on what packages to install can be found here: https://www.youtube.com/watch?v=0kpGcMjpDcw

Future features:
-----------
 - add a simple logic to trigger the watering only when needed (eg: not trigger when scheduled if the soil is already wet, or if the weather forecast for your area announces rain with a probability higher than a certain threshold etc.)
 - ability to *program* the watering schedule in the Google calendar by simply adding events the the system's calendar

What you need:
--------------
 - Raspberry Pi board (I used an older Raspberry Pi 1 Model B revision 1.2)
 - (only if you need remote access to the Raspberry or if the webpage mode is used) a WiFi Dongle. Check this compatibility list before buying! https://elinux.org/RPi_USB_Wi-Fi_Adapters
 - a 8Gb SD card with Raspbian
 - a relay to swotch the water pump (I used this one: https://www.amazon.de/gp/product/B00PIMRGN4)
 - a submersible water pump (http://www.ebay.de/itm/Comet-Tauchpumpe-ELEGANT-12V-Trinkwasserpumpe-Frischwasserpumpe-Kanisterpumpe)
 - a 12V DC power adapter (used to power up both the water pump AND the Raspberry Pi! - for instance this one: http://www.ebay.de/itm/DC-12V-1A-10A-LED-Trafo-Netzteil-Netzadapter-Driver-fur-LED-RGB-Strip-Streifen-/331515528752?var=&hash=item4d2fdd8630:g:pmEAAOSwjVVVsdUu)
 - a 5V UBEC to feed power to the Raspberry Pi (http://www.ebay.de/itm/Hobbywing-3A-5V-6V-BEC-UBEC-Einlangsspannung-5-5-26V-2-6-S-Lipo-SBEC-Akku-G-221-/142048845232?_trksid=p2385738.m2548.l4275)
 - 10mm plastic tube (https://www.ebay.de/sch/sis.html?_itemId=null&_nkw=PVC+Schlauch+glasklar+Aquariumschlauch+Luftschlauch+versch+in+5m+Laengen)
 - 20x Gardena micro drippers (https://www.amazon.de/Gardena-1391-20-Micro-Drip-System-Regulierbarer-Endtropfer/dp/B0001E3S9U)
 - a water tank (depending on your needs, I used a 60l one: http://www.ebay.de/itm/25-40-60-L-Fass-Weithalsfass-Vorratsfass-Transporttonne-Fass-Camping-Outdoor)
 - a waterproof case big enough to contain all the hardware
 - cable outlets for the box (http://www.ebay.de/itm/Kabelverschraubung-M12-x-1-5-mm-IP67-10x-St%C3%BCck-Verschraubung-3-6-5-mm-grau)
 - various connectors for the water tubing (http://www.ebay.de/itm/Schlauchverbinder-Kunststoff-Druckluft-Luft-Y-St%C3%BCck-T-St%C3%BCck-Kreuz-Winkel)
 - 2-wire waterproof electrical connectors (https://www.amazon.de/gp/product/B0171FEI1I)
 
Optional (not used yet by the software in this project, but everything already prepared)
------------------------------------------------------------------------
 - 2x soil humidity sensors (http://www.ebay.de/itm/2-St%C3%BCck-Wasserstandssensor-Hygrometer-Bodenfeuchte-Sensor-Feuchtigkeitssensor)
 - 1x DHT11 temperature/humidity sensor - used to monitor the inside of the box (http://www.ebay.de/itm/DHT11-Temperatur-messen-Luftfeuchtigkeit-Sensor-Modul-Raspberry-Pi-Arduino)
 - 1x AM2302 temperature/humidity sensor - used to monitor the outside of the box (http://www.ebay.de/itm/AM2320B-AM2320-DHT22-AM2302-Digital-Feuchtigkeit-Feuchte-Temperatur)
  - 1x ON-ON waterproof switch (https://www.amazon.de/gp/product/B008IBN07S)
  - several 5mm LEDs, different colors (http://www.ebay.de/itm/Leuchtdiode-5mm-LED-Sortiment-diffus-klar-verschiedene-St%C3%BCckzahl-f%C3%BCr-Arduino)
  - waterproof holders for the LEDs (https://www.amazon.de/gp/product/B00KHTVM8S)

How to install GoWaterPi
------------------------------------------------------------------------
1. Install latest Raspbian on an SD card, put into Raspberry Pi and configure it
2. Get GoWaterPi repository:
```
        git clone https://github.com/Contrasens/GoWaterPi.git
```
3. Install ADAFRUIT_DHT for Python2:
```
        sudo apt-get update
        sudo apt-get install python-pip
        sudo python -m pip install --upgrade pip setuptools wheel
        sudo pip install Adafruit_DHT
```
3. Install graphical tools for editing cron jobs (together with other useful packages):

```
        sudo apt-get install gnome-schedule
```
        
4. Edit crontab to add an entry to execute (in this example everyday at 19:00):
```
        0 19 * * * python /home/pi/GoWaterPi/autoWater.py
```
5. Edit crontab to send an email everytime when plants get water:
```
        0 19 * * * python /home/pi/GoWaterPi/send_email.py
```
6. Edit send_email.py and add the email account to send email from and its password
7. Tweak the config parameters from config.py (as is, the plants will be watered for 200 seconds)
