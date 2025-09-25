from config.db import db
import uuid
import datetime

class Rating(db.Model):
    __tablename__ = 'ratings'

    id_rating = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    rate = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    date = db.Column(db.Date, default=datetime.date.today, nullable=False)

    def __init__(self, rate, comment, date):
        self.rate = rate
        self.comment = comment
        self.date = date

    def to_json(self):
        return {
            'id_rating': self.id_rating,
            'rate': self.rate,
            'comment': self.comment,
            'date': self.date
        }