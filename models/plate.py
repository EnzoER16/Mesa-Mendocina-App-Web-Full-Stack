from config.db import db
import uuid

class Plate(db.Model):
    __tablename__ = 'plates'

    id_plate = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)

    # FK a Location
    id_location = db.Column(db.String(36), db.ForeignKey("locations.id_location"), nullable=False)

    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

    def to_json(self):
        return {
            'id_plate': self.id_plate,
            'name': self.name,
            'description': self.description,
            'price': self.price
        }