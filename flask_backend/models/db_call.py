from flask_backend import db


class DBCall(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Not storing the phone number!

    timestamp = db.Column(db.DateTime)

    language = db.Column(db.String)    # "" if not answered
    answer_1 = db.Column(db.Integer)    #  0 if not answered
    answer_2 = db.Column(db.Integer)    #  0 if not answered
    zip_code = db.Column(db.String)          # "" if not answered

    def __repr__(self):
        return f"DBCall(id: {self.id}, " \
               f"timestamp: {self.timestamp.strftime('%d.%m.%Y, %H:%M:%S')}, " \
               f"language: \"{self.language}\", " \
               f"answer_1: {self.answer_1}, " \
               f"answer_2: {self.answer_2}, " \
               f"zip_code: \"{self.zip_code}\")"


