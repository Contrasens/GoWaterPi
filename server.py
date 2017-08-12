from flask import Flask, render_template, request, jsonify
import Pins
import config

app = Flask(__name__)


# return index page when IP address of RPi is typed in the browser
@app.route("/")
def index():
    return render_template("index.html", uptime=getUptime())


# ajax GET call this function to set yellow led state
# depending on the GET parameter sent
@app.route("/_ledYellow")
def _ledYellow():
    state = request.args.get('state')
    if state == "auto":
        Pins.ledOn(config.YELLOW_LED_PIN)
        print "Yellow - Auto"
    if state == "manual":
        Pins.ledOff(config.YELLOW_LED_PIN)
        print "Yellow - Manual"
    return ""


# ajax GET call this function to set green led state
# depending on the GET parameter sent
@app.route("/_ledGreen")
def _ledGreen():
    state = request.args.get('state')
    if state == "auto":
        Pins.ledOff(config.GREEN_LED_PIN)
        print "Green - Auto"
    if state == "manual":
        Pins.ledOn(config.GREEN_LED_PIN)
        print "Green - Manual"
    return ""


# ajax GET call this function periodically to read button state
# the state is sent back as json data
@app.route("/_button")
def _button():
    if Pins.readState():
        state = "active"
    else:
        state = "not active"
    return jsonify(buttonState=state)


def getUptime():
    # get uptime from the linux terminal command
    from subprocess import check_output
    output = check_output(["uptime"])
    # return only uptime info
    uptime = output[output.find("up"):output.find("user") - 5]
    return uptime


# run the webserver, requires sudo
if __name__ == "__main__":
    Pins.init()
    app.run(host=config.SERVER_IP, port=config.PORT, debug=True)