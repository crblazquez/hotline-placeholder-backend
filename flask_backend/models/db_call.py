from flask_backend import db
from datetime import datetime


class DBCall(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Not storing the phone number!

    timestamp = db.Column(db.DateTime)
    answer_1 = db.Column(db.String)     # 0 if not answered
    answer_2 = db.Column(db.String)     # 0 if not answered
    zip = db.Column(db.String)          # "" if not answered

    def __repr__(self):
        return f"DBCall(id: {self.id})"
