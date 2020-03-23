
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

    # If Twilio's request to our app included already gathered digits,
    # process them
    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']

        # <Say> a different message depending on the caller's choice
        if choice == '1':
            resp.redirect('/german/initial')
            return str(resp)
        elif choice == '2':
            resp.redirect('/english/initial')
            return str(resp)
        else:
            # If the caller didn't choose 1 or 2, apologize and ask them again
            resp.say("Es tut mir Leid, das habe ich leider nicht verstanden", voice="woman", language="de")
            resp.say("Sorry, I didn't understand that choice.", voice="woman", language="en-gb")

    # Start our <Gather> verb
    gather = Gather(num_digits=1)
    gather.say('Wenn sie auf Deutsch verbunden werden möchten, drücken Sie bitte die 1', voice="woman", language="de")
    gather.say('If you would like to be connected in english, press 2', voice="woman", language="en-gb")
    resp.append(gather)

    # If the user doesn't select an option, redirect them into a loop
    resp.redirect('/hotline')

    return str(resp)


@app.route("/german/initial", methods=['GET', 'POST'])
def german_initial():
    # Start our TwiML response
    resp = VoiceResponse()

    # Read a message aloud to the caller
    resp.say("Vielen Dank für Ihren Anruf und Ihr Interesse! " +
             "Da sich unser Dienst erst in der Entwicklungsphase befindet, " +
             "bekommen Sie auf diese Anfrage noch keinen Rückruf.", voice="woman", language="de")

    return str(resp)


@app.route("/english/initial", methods=['GET', 'POST'])
def english_initial():
    # Start our TwiML response
    resp = VoiceResponse()

    # Read a message aloud to the caller

    resp.say("Thank you for calling and being interested in our service. " +
             "Since our services are still in development, this call will not " +
             "be answered.", voice="woman", language="en-gb")

    return str(resp)
