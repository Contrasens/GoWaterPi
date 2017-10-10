# GoWaterPi
A plant irigation system based on Raspberry Pi, either manual or at scheduled intervals. A submersible water pump is started to water the plants, then stopped after a configurable time interval.

Currently, a Python script is started by a Cron job at predifined intervals (see http://www.adminschoice.com/crontab-quick-reference). The Python script starts the water pump and keeps it running for a time priod which is specified in a configuration file.

The web-page branch can be used to monitor the activity of the watering system over the internet, and switch it on and off remotely. A web-server must be set up, and the server port must be opened in your router to be able to access it from remote locations. Of course, then a wireless USB dongle is needed, which is able to work from inside the case.

Future features:
- a simple logic to trigger the watering only when needed (eg: not trigger when scheduled if the soil is already wet, or if the weather forecast for your area announces rain with a probability higher than a certain threshold etc.)
- program the watering schedule in the Google calendar by simply adding events the the system's calendar
- get the system send emails at important events (eg: watering successfully finished, cancelled due to wet soil/upcoming rain, reminders to refill the water tank etc.)

What you need:
 - Raspberry Pi board (I used an older Raspberry Pi 1 Model B revision 1.2)
 - a 8Gb SD card with Raspbian
 - a relay to swotch the water pump (I used this one: https://www.amazon.de/gp/product/B00PIMRGN4/ref=oh_aui_detailpage_o06_s01?ie=UTF8&psc=1)
 - a submersible water pump (http://www.ebay.de/itm/Comet-Tauchpumpe-ELEGANT-12V-Trinkwasserpumpe-Frischwasserpumpe-Kanisterpumpe)
 - a 12V DC power adapter (used to power up both the water pump AND the Raspberry Pi!)
 - 10mm plastic tube (https://www.ebay.de/sch/sis.html?_itemId=null&_nkw=PVC+Schlauch+glasklar+Aquariumschlauch+Luftschlauch+versch+in+5m+Laengen&_trksid=p2047675.m4100.l9146)
 - a water tank (depending on your needs, I used a 60l one: http://www.ebay.de/itm/25-40-60-L-Fass-Weithalsfass-Vorratsfass-Transporttonne-Fass-Camping-Outdoor/302264338555?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2060353.m2749.l2649)
 - a waterproof case big enough to contain all the hardware
 - cable outlets for the box (http://www.ebay.de/itm/Kabelverschraubung-M12-x-1-5-mm-IP67-10x-St%C3%BCck-Verschraubung-3-6-5-mm-grau/172374887740?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2060353.m2749.l2649)
 - various connectors for the water tubing (http://www.ebay.de/itm/Schlauchverbinder-Kunststoff-Druckluft-Luft-Y-St%C3%BCck-T-St%C3%BCck-Kreuz-Winkel/221585628836?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2060353.m2749.l2649)
 - 2-wire waterproof electrical connectors (https://www.amazon.de/gp/product/B0171FEI1I/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1)
 
 Optional (not used yet by the software in this project, but already prepared for it)
 - 2x soil humidity sensors (http://www.ebay.de/itm/2-St%C3%BCck-Wasserstandssensor-Hygrometer-Bodenfeuchte-Sensor-Feuchtigkeitssensor/172510446407?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2060353.m2749.l2649)
 - 1x DHT11 temperature/humidity sensor - used to monitor the inside of the box (http://www.ebay.de/itm/DHT11-Temperatur-messen-Luftfeuchtigkeit-Sensor-Modul-Raspberry-Pi-Arduino/252798960892?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2060353.m2749.l2649)
 - 1x AM2302 temperature/humidity sensor - used to monitor the outside of the box (http://www.ebay.de/itm/AM2320B-AM2320-DHT22-AM2302-Digital-Feuchtigkeit-Feuchte-Temperatur/322619338796?ssPageName=STRK%3AMEBIDX%3AIT&var=511617316584&_trksid=p2060353.m2749.l2649)
  - 1x ON-ON waterproof switch (https://www.amazon.de/gp/product/B008IBN07S/ref=oh_aui_detailpage_o04_s00?ie=UTF8&psc=1)
  - several 5mm LEDs, different colors (http://www.ebay.de/itm/Leuchtdiode-5mm-LED-Sortiment-diffus-klar-verschiedene-St%C3%BCckzahl-f%C3%BCr-Arduino/182658283643?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2060353.m2749.l2649)
  - waterproof holders for the LEDs (https://www.amazon.de/gp/product/B00KHTVM8S/ref=oh_aui_detailpage_o04_s00?ie=UTF8&psc=1)
