from config.db import db
import uuid

class Rating(db.Model):
    __tablename__ = 'ratings'

    id_rating = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_user = db.Column(db.String(36), nullable=False)
    id_location = db.Column(db.String(36), nullable=False)
    punctuation = db.Column(db.String(36), nullable=False)
    comment = db.Column(db.String(36), nullable=False)
    date = db.Column(db.String(36), nullable=False)

    def __init__(self, id_user, id_location, punctuation, comment, date):
        self.id_user = id_user
        self.id_location = id_location
        self.punctuation = punctuation
        self.comment = comment
        self.date = date

    def to_json(self):
        return {
            'id_rating': self.id_rating,
            'id_user': self.id_user,
            'id_location': self.id_location,
            'punctuation': self.punctuation,
            'comment': self.comment,
            'date': self.date
        }