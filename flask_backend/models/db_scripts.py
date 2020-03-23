
from flask_backend import db
from flask_backend.models.db_call import DBCall

from datetime import datetime


def create_call():
    call = DBCall()
    call.timestamp = datetime.now()
    call.language = ""
    call.answer_1 = 0
    call.answer_2 = 0
    call.zip_code = ""

    db.session.add(call)

    db.session.flush()
    call_id = call.id

    db.session.commit()

    return call_id


def edit_call(call_id, key, value):
    call = DBCall.query.filter(DBCall.id == call_id).first()

    if (call is not None) and (key in ["language", "answer_1", "answer_2", "zip_code"]):
        if key == "language":
            call.language = value
        elif key == "answer_1":
            call.answer_1 = value
        elif key == "answer_2":
            call.answer_2 = value
        else:
            call.zip_code = value

    db.session.commit()


if __name__ == "__main__":
    test_call_id = create_call()

    print(test_call_id)

    edit_call(test_call_id, "language", "deutsch")
    edit_call(test_call_id, "answer_1", 1)
    edit_call(test_call_id, "answer_2", 2)
    edit_call(test_call_id, "zip_code", "50328")

    calls = DBCall.query.all()

    for call in calls:
        print(call)

