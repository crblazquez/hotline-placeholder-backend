
from flask import request
from flask_backend import app
from twilio.twiml.voice_response import VoiceResponse, Gather


@app.route("/")
def hello():
    return "Hilfe am Ohr Hotline. See our <a href='https://www.hilfe-am-ohr.de/'>Website</a> for more."


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

    resp.say("Wenn sie unseren Dienst unterstützen möchten, können sie uns jetzt schon " +
             "drei kurze Fragen beantworten. Falls Sie dies nicht tun möchten, legen Sie einfach auf.", voice="woman", language="de")

    resp.redirect('/german/question/1')

    return str(resp)


@app.route("/english/initial", methods=['GET', 'POST'])
def english_initial():
    # Start our TwiML response
    resp = VoiceResponse()

    # Read a message aloud to the caller

    resp.say("Thank you for calling and being interested in our service. " +
             "Since our services are still in development, this call will not " +
             "be answered.", voice="woman", language="en-gb")

    resp.say("If you want to support us on our journey, you can answer three short questions for us. " +
             "If you don't want that, you can just hang up.", voice="woman", language="en-gb")

    resp.redirect('/english/question/1')

    return str(resp)


@app.route("/german/question/1", methods=['GET', 'POST'])
def german_question_1():
    # Start our TwiML response
    resp = VoiceResponse()

    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']

        # <Say> a different message depending on the caller's choice
        if choice == '1':
            resp.say("Vielen Dank für Ihr Interesse!", voice="woman", language="de")
            resp.redirect("/german/question/2")
            return str(resp)
        elif choice == '2':
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

    resp.redirect('/german/question/1')

    return str(resp)


@app.route("/german/question/2", methods=['GET', 'POST'])
def german_question_2():
    # Start our TwiML response
    resp = VoiceResponse()

    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']

        # <Say> a different message depending on the caller's choice
        if choice in ["1", "2"]:
            # TODO: Save in Database
            resp.redirect("/german/question/3")
            return str(resp)
        else:
            # If the caller didn't choose 1 or 2, apologize and ask them again
            resp.say("Es tut mir Leid, das habe ich leider nicht verstanden", voice="woman", language="de")

    gather = Gather(num_digits=1)
    gather.say("Würden Sie dies als Anrufer oder als freiwilliger Helfer tun?", voice="woman", language="de")
    gather.say("Drücken Sie 1 für Anrufer. Drücken sie 2 für Helfer.", voice="woman", language="de")
    resp.append(gather)

    resp.redirect('/german/question/2')

    return str(resp)


@app.route("/german/question/3", methods=['GET', 'POST'])
def german_question_3():
    # Start our TwiML response
    resp = VoiceResponse()
    gather = Gather(num_digits=6, finish_on_key="#")

    if 'Digits' in request.values:
        # Get which digit the caller chose
        digits = request.values['Digits']
        finished_on_key = request.values['FinishedOnKey']

        if len(digits) == 5 and finished_on_key == "#":
            # TODO: Save in Database
            resp.say("Vielen Dank für Ihre Teilnahme! Auf Wiederhören!", voice="woman", language="de")
            return str(resp)
        else:
            gather.say("Bitte geben Sie ihre Postleitzahl an.", voice="woman", language="de")
    else:
        gather.say("Sie können uns noch mehr unterstützen, indem Sie ihre Postleitzahl angeben.", voice="woman", language="de")

    gather.say("Bestätigen Sie die Postleitzahl mit der Raute-Taste.", voice="woman", language="de")
    gather.say("Um von vorne zu beginnen, warten Sie einfach ab.", voice="woman", language="de")
    resp.append(gather)

    resp.redirect('/german/question/3')

    return str(resp)


@app.route("/english/question/1", methods=['GET', 'POST'])
def english_question_1():
    # Start our TwiML response
    resp = VoiceResponse()

    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']

        # <Say> a different message depending on the caller's choice
        if choice == '1':
            resp.say("Thank you for your interest!", voice="woman", language="en-gb")
            resp.redirect("/english/question/2")
            return str(resp)
        elif choice == '2':
            resp.say('Thank you for your call! Goodbye!', voice="woman", language="en-gb")
            return str(resp)
        else:
            # If the caller didn't choose 1 or 2, apologize and ask them again
            resp.say("Sorry, I didn't understand that choice.", voice="woman", language="en-gb")

    gather = Gather(num_digits=1)
    gather.say("Would you make use of our services, either as a caller or as a volunteer?", voice="woman", language="en-gb")
    gather.say("Press 1 for yes. Press 2 for no.", voice="woman", language="en-gb")
    resp.append(gather)

    resp.redirect('/english/question/1')

    return str(resp)


@app.route("/english/question/2", methods=['GET', 'POST'])
def english_question_2():
    # Start our TwiML response
    resp = VoiceResponse()

    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']

        # <Say> a different message depending on the caller's choice
        if choice in ["1", "2"]:
            # TODO: Save in Database
            resp.redirect("/english/question/3")
            return str(resp)
        else:
            # If the caller didn't choose 1 or 2, apologize and ask them again
            resp.say("Sorry, I didn't understand that choice.", voice="woman", language="en-gb")

    gather = Gather(num_digits=1)
    gather.say("If so, as a caller or as a volunteer?", voice="woman", language="en-gb")
    gather.say("Press 1 for caller. Press 2 for volunteer.", voice="woman", language="en-gb")
    resp.append(gather)

    resp.redirect('/english/question/2')

    return str(resp)


@app.route("/english/question/3", methods=['GET', 'POST'])
def english_question_3():
    # Start our TwiML response
    resp = VoiceResponse()
    gather = Gather(num_digits=6, finish_on_key="#")

    if 'Digits' in request.values:
        # Get which digit the caller chose
        digits = request.values['Digits']
        finished_on_key = request.values['FinishedOnKey']

        if len(digits) == 5 and finished_on_key == "#":
            # TODO: Save in Database
            resp.say("Thank your for your contribution! Goodbye!", voice="woman", language="en-gb")
            return str(resp)
        else:
            gather.say("Please enter your zip code.", voice="woman", language="en-gb")
    else:
        gather.say("You can support us even more, if you enter your zip code.", voice="woman", language="en-gb")

    gather.say("Please confirm, by using the hash-key.", voice="woman", language="en-gb")
    gather.say("To start over, just hold the line", voice="woman", language="en-gb")
    resp.append(gather)

    resp.redirect('/english/question/3')

    return str(resp)
