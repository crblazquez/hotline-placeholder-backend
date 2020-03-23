
from flask import request
from flask_backend import app
from twilio.twiml.voice_response import VoiceResponse, Gather

from flask_backend.models.db_scripts import create_call, edit_call


@app.route("/")
def hello():
    return "<p>\"Hilfe am Ohr\" Hotline. See our <a href='https://www.hilfe-am-ohr.de/'>Website</a> for more.</p>"


@app.route("/hotline", methods=['GET', 'POST'])
def initial_endpoint():
    call_id = create_call()
    resp = VoiceResponse()
    resp.redirect(f'/hotline/{call_id}')
    return str(resp)


@app.route("/hotline/<call_id>", methods=['GET', 'POST'])
def endpoint_with_id(call_id):

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
            edit_call(call_id, "language", "deutsch")
            resp.redirect(f'/german/initial/{call_id}')
            return str(resp)
        elif choice == '2':
            edit_call(call_id, "language", "english")
            resp.redirect(f'/english/initial/{call_id}')
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
    resp.redirect(f'/hotline/{call_id}')

    return str(resp)


@app.route("/german/initial/<call_id>", methods=['GET', 'POST'])
def german_initial(call_id):
    # Start our TwiML response
    resp = VoiceResponse()

    # Read a message aloud to the caller
    resp.say("Vielen Dank für Ihren Anruf und Ihr Interesse! " +
             "Da sich unser Dienst erst in der Entwicklungsphase befindet, " +
             "bekommen Sie auf diese Anfrage noch keinen Rückruf.", voice="woman", language="de")

    resp.say("Wenn sie unseren Dienst unterstützen möchten, können sie uns jetzt schon " +
             "drei kurze Fragen beantworten. Falls Sie dies nicht tun möchten, legen Sie einfach auf.", voice="woman", language="de")

    resp.redirect(f'/german/question/1/{call_id}')

    return str(resp)


@app.route("/english/initial/<call_id>", methods=['GET', 'POST'])
def english_initial(call_id):
    # Start our TwiML response
    resp = VoiceResponse()

    # Read a message aloud to the caller

    resp.say("Thank you for calling and being interested in our service. " +
             "Since our services are still in development, this call will not " +
             "be answered.", voice="woman", language="en-gb")

    resp.say("If you want to support us on our journey, you can answer three short questions for us. " +
             "If you don't want that, you can just hang up.", voice="woman", language="en-gb")

    resp.redirect(f'/english/question/1/{call_id}')

    return str(resp)


@app.route("/german/question/1/<call_id>", methods=['GET', 'POST'])
def german_question_1(call_id):
    # Start our TwiML response
    resp = VoiceResponse()

    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']

        # <Say> a different message depending on the caller's choice
        if choice == '1':
            edit_call(call_id, "answer_1", 1)
            resp.say("Vielen Dank für Ihr Interesse!", voice="woman", language="de")
            resp.redirect(f"/german/question/2/{call_id}")
            return str(resp)
        elif choice == '2':
            edit_call(call_id, "answer_1", 2)
            resp.say('Vielen Dank für ihren Anruf! Auf Wiederhören!', voice="woman", language="de")
            return str(resp)
        else:
            # If the caller didn't choose 1 or 2, apologize and ask them again
            resp.say("Es tut mir Leid, das habe ich leider nicht verstanden", voice="woman", language="de")

    gather = Gather(num_digits=1)
    gather.say("Würden Sie unseren Dienst als Anrufer oder als freiwilliger "
               "Helfer in Anspruch nehmen?", voice="woman", language="de")
    gather.say("Drücken Sie 1 für ja. Drücken sie 2 für nein.", voice="woman", language="de")
    resp.append(gather)

    resp.redirect(f'/german/question/1/{call_id}')

    return str(resp)


@app.route("/german/question/2/<call_id>", methods=['GET', 'POST'])
def german_question_2(call_id):
    # Start our TwiML response
    resp = VoiceResponse()

    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']

        # <Say> a different message depending on the caller's choice
        if choice in ["1", "2"]:
            edit_call(call_id, "answer_2", int(choice))
            resp.redirect(f"/german/question/3/{call_id}")
            return str(resp)
        else:
            # If the caller didn't choose 1 or 2, apologize and ask them again
            resp.say("Es tut mir Leid, das habe ich leider nicht verstanden", voice="woman", language="de")

    gather = Gather(num_digits=1)
    gather.say("Würden Sie dies als Anrufer oder als freiwilliger Helfer tun?", voice="woman", language="de")
    gather.say("Drücken Sie 1 für Anrufer. Drücken sie 2 für Helfer.", voice="woman", language="de")
    resp.append(gather)

    resp.redirect(f'/german/question/2/{call_id}')

    return str(resp)


@app.route("/german/question/3/<call_id>", methods=['GET', 'POST'])
def german_question_3(call_id):
    # Start our TwiML response
    resp = VoiceResponse()
    gather = Gather(num_digits=6, finish_on_key="#")

    if 'Digits' in request.values:
        # Get which digit the caller chose
        digits = request.values['Digits']
        finished_on_key = request.values['FinishedOnKey']

        if len(digits) == 5 and finished_on_key == "#":
            edit_call(call_id, "zip_code", digits)
            resp.say("Vielen Dank für Ihre Teilnahme! Auf Wiederhören!", voice="woman", language="de")
            return str(resp)
        else:
            gather.say("Bitte geben Sie ihre Postleitzahl an.", voice="woman", language="de")
    else:
        gather.say("Sie können uns noch mehr unterstützen, indem Sie ihre Postleitzahl angeben.", voice="woman", language="de")

    gather.say("Bestätigen Sie die Postleitzahl mit der Raute-Taste.", voice="woman", language="de")
    gather.say("Um von vorne zu beginnen, warten Sie einfach ab.", voice="woman", language="de")
    resp.append(gather)

    resp.redirect(f'/german/question/3/{call_id}')

    return str(resp)


@app.route("/english/question/1/<call_id>", methods=['GET', 'POST'])
def english_question_1(call_id):
    # Start our TwiML response
    resp = VoiceResponse()

    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']

        # <Say> a different message depending on the caller's choice
        if choice == '1':
            edit_call(call_id, "answer_1", 1)
            resp.say("Thank you for your interest!", voice="woman", language="en-gb")
            resp.redirect(f"/english/question/2/{call_id}")
            return str(resp)
        elif choice == '2':
            edit_call(call_id, "answer_1", 2)
            resp.say('Thank you for your call! Goodbye!', voice="woman", language="en-gb")
            return str(resp)
        else:
            # If the caller didn't choose 1 or 2, apologize and ask them again
            resp.say("Sorry, I didn't understand that choice.", voice="woman", language="en-gb")

    gather = Gather(num_digits=1)
    gather.say("Would you make use of our services, either as a caller or as a volunteer?", voice="woman", language="en-gb")
    gather.say("Press 1 for yes. Press 2 for no.", voice="woman", language="en-gb")
    resp.append(gather)

    resp.redirect(f'/english/question/1/{call_id}')

    return str(resp)


@app.route("/english/question/2/<call_id>", methods=['GET', 'POST'])
def english_question_2(call_id):
    # Start our TwiML response
    resp = VoiceResponse()

    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']

        # <Say> a different message depending on the caller's choice
        if choice in ["1", "2"]:
            edit_call(call_id, "answer_2", int(choice))
            resp.redirect(f"/english/question/3/{call_id}")
            return str(resp)
        else:
            # If the caller didn't choose 1 or 2, apologize and ask them again
            resp.say("Sorry, I didn't understand that choice.", voice="woman", language="en-gb")

    gather = Gather(num_digits=1)
    gather.say("If so, as a caller or as a volunteer?", voice="woman", language="en-gb")
    gather.say("Press 1 for caller. Press 2 for volunteer.", voice="woman", language="en-gb")
    resp.append(gather)

    resp.redirect(f'/english/question/2/{call_id}')

    return str(resp)


@app.route("/english/question/3/<call_id>", methods=['GET', 'POST'])
def english_question_3(call_id):
    # Start our TwiML response
    resp = VoiceResponse()
    gather = Gather(num_digits=6, finish_on_key="#")

    if 'Digits' in request.values:
        # Get which digit the caller chose
        digits = request.values['Digits']
        finished_on_key = request.values['FinishedOnKey']

        if len(digits) == 5 and finished_on_key == "#":
            edit_call(call_id, "zip_code", digits)
            resp.say("Thank your for your contribution! Goodbye!", voice="woman", language="en-gb")
            return str(resp)
        else:
            gather.say("Please enter your zip code.", voice="woman", language="en-gb")
    else:
        gather.say("You can support us even more, if you enter your zip code.", voice="woman", language="en-gb")

    gather.say("Please confirm, by using the hash-key.", voice="woman", language="en-gb")
    gather.say("To start over, just hold the line", voice="woman", language="en-gb")
    resp.append(gather)

    resp.redirect(f'/english/question/3/{call_id}')

    return str(resp)
