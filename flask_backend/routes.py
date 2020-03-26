
from flask import request
from flask_backend import app
from twilio.twiml.voice_response import VoiceResponse, Gather

from flask_backend.models.db_scripts import create_call, edit_call

from flask_backend.hotline_translation import hotline_translation


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
def endpoint_with_call_id(call_id):

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
            edit_call(call_id, "language", "de")
            resp.redirect(f'/hotline/de/initial/{call_id}')
            return str(resp)
        elif choice == '2':
            edit_call(call_id, "language", "en-gb")
            resp.redirect(f'/hotline/en-gb/initial/{call_id}')
            return str(resp)
        else:
            # If the caller didn't choose 1 or 2, apologize and ask them again
            resp.say(hotline_translation["choose_language_unknown"]["de"], voice="woman", language="de")
            resp.say(hotline_translation["choose_language_unknown"]["en-gb"], voice="woman", language="en-gb")

    # Start our <Gather> verb
    gather = Gather(num_digits=1)
    gather.say(hotline_translation["choose_language"]["de"], voice="woman", language="de")
    gather.say(hotline_translation["choose_language"]["en-gb"], voice="woman", language="en-gb")
    resp.append(gather)

    # If the user doesn't select an option, redirect them into a loop
    resp.redirect(f'/hotline/{call_id}')

    return str(resp)


@app.route("/hotline/<language>/initial/<call_id>", methods=['GET', 'POST'])
def endpoint_with_language(language, call_id):
    # Start our TwiML response
    resp = VoiceResponse()

    # Read a message aloud to the caller
    resp.say(hotline_translation["text_1"][language], voice="woman", language=language)
    resp.say(hotline_translation["text_2"][language], voice="woman", language=language)

    resp.redirect(f'/hotline/{language}/question/1/{call_id}')

    return str(resp)


@app.route("/hotline/<language>/question/1/<call_id>", methods=['GET', 'POST'])
def german_question_1(language, call_id):
    # Start our TwiML response
    resp = VoiceResponse()

    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']

        # <Say> a different message depending on the caller's choice
        if choice == '1':
            edit_call(call_id, "answer_1", 1)
            resp.say(hotline_translation["question_1_answer_yes"][language], voice="woman", language=language)
            resp.redirect(f"/hotline/{language}/question/2/{call_id}")
            return str(resp)
        elif choice == '2':
            edit_call(call_id, "answer_1", 2)
            resp.say(hotline_translation["question_1_answer_no"][language], voice="woman", language=language)
            return str(resp)
        else:
            # If the caller didn't choose 1 or 2, apologize and ask them again
            resp.say(hotline_translation["question_1_answer_unknown"][language], voice="woman", language=language)

    gather = Gather(num_digits=1)
    gather.say(hotline_translation["question_1_text_1"][language], voice="woman", language=language)
    resp.append(gather)

    resp.redirect(f'/hotline/{language}/question/1/{call_id}')

    return str(resp)


@app.route("/hotline/<language>/question/2/<call_id>", methods=['GET', 'POST'])
def german_question_2(language, call_id):
    # Start our TwiML response
    resp = VoiceResponse()

    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']

        # <Say> a different message depending on the caller's choice
        if choice in ["1", "2"]:
            edit_call(call_id, "answer_2", int(choice))
            resp.redirect(f"/hotline/{language}/question/3/{call_id}")
            return str(resp)
        else:
            # If the caller didn't choose 1 or 2, apologize and ask them again
            resp.say(hotline_translation["question_2_answer_unknown"][language], voice="woman", language=language)

    gather = Gather(num_digits=1)
    gather.say(hotline_translation["question_2_text_1"][language], voice="woman", language=language)
    resp.append(gather)

    resp.redirect(f'/hotline/{language}/question/2/{call_id}')

    return str(resp)


@app.route("/hotline/<language>/question/3/<call_id>", methods=['GET', 'POST'])
def german_question_3(language, call_id):
    # Start our TwiML response
    resp = VoiceResponse()
    gather = Gather(num_digits=6, finish_on_key="#")

    if 'Digits' in request.values:
        # Get which digit the caller chose
        digits = request.values['Digits']
        finished_on_key = request.values['FinishedOnKey']

        if len(digits) == 5 and finished_on_key == "#":
            edit_call(call_id, "zip_code", digits)
            resp.say(hotline_translation["question_3_answer_yes"][language], voice="woman", language=language)
            return str(resp)
        else:
            gather.say(hotline_translation["question_3_answer_unknown"][language], voice="woman", language=language)
    else:
        gather.say(hotline_translation["question_3_text_1"][language], voice="woman", language=language)

    gather.say(hotline_translation["question_3_text_2"][language], voice="woman", language=language)
    resp.append(gather)

    resp.redirect(f'/hotline/{language}/question/3/{call_id}')

    return str(resp)

