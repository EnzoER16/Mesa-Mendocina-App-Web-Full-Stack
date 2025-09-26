from config.db import db
import uuid
import datetime

class Rating(db.Model):
    __tablename__ = 'ratings'

    id_rating = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    rate = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    date = db.Column(db.Date, default=datetime.date.today, nullable=False)

    id_user = db.Column(db.String(36), db.ForeignKey("users.id_user"), nullable=False)
    id_location = db.Column(db.String(36), db.ForeignKey("locations.id_location"), nullable=False)

    def __init__(self, rate, comment, date, id_user, id_location):
        self.rate = rate
        self.comment = comment
        self.date = date
        self.id_user = id_user
        self.id_location = id_user

    def to_json(self):
        return {
            'id_rating': self.id_rating,
            'rate': self.rate,
            'comment': self.comment,
            'date': self.date,
            'id_user': self.id_user,
            'id_location': self.id_location
        }