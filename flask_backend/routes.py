
from flask import request
from flask_backend import app
from twilio.twiml.voice_response import VoiceResponse, Gather


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/hotline", methods=['GET', 'POST'])
def initial_endpoint():
    """Respond to incoming phone calls with a menu of options"""
    # Start our TwiML response
    resp = VoiceResponse()

    resp.say("Willkommen bei Hilfe am Ohr!", voice="woman", language="de")

    return str(resp)
