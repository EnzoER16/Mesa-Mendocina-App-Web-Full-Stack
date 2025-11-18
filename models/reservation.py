from config.db import db
from sqlalchemy import Enum
import datetime
import uuid

class Reservation(db.Model):
    __tablename__ = 'reservations'

    id_reservation = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    date = db.Column(db.Date, default=datetime.date.today, nullable=False)
    time = db.Column(db.Time, nullable=False)
    people = db.Column(db.Integer, nullable=False)
    status = db.Column(Enum('pending', 'accepted', 'rejected', 'cancelled', name='reservation_status'), default='pending')
    image = db.Column(db.String(200), nullable=True, default="no_image.png")

    id_user = db.Column(db.String(36), db.ForeignKey("users.id_user"), nullable=False)
    id_location = db.Column(db.String(36), db.ForeignKey("locations.id_location"), nullable=False)

    def __init__(self, date, time, people, id_user, id_location, status="pending"):
        self.date = date
        self.time = time
        self.people = people
        self.id_user = id_user
        self.id_location = id_location
        self.status = status
    
    def to_json(self):
        return {
            'id_reservation': self.id_reservation,
            'date': self.date.strftime('%Y-%m-%d') if self.date else None,
            'time': self.time.strftime('%H:%M:%S') if self.time else None,
            'people': self.people,
            'status': self.status,
            'id_user': self.id_user,
            'id_location': self.id_location
        }