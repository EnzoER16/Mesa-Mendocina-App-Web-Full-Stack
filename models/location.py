from config.db import db
import uuid

class Location(db.Model):
    __tablename__ = 'locations'

    id_location = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    schedule = db.Column(db.String(100), nullable=False)
    price_range = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(50), unique=True, nullable=False)

    id_user = db.Column(db.String(36), db.ForeignKey("users.id_user"), nullable=False)

    plates = db.relationship("Plate", backref="location", lazy=True)
    ratings = db.relationship("Rating", backref="location", lazy=True)

    def __init__(self, name, address, department, schedule, price_range, phone, id_user):
        self.name = name
        self.address = address
        self.department = department
        self.schedule = schedule
        self.price_range = price_range
        self.phone = phone
        self.id_user = id_user

    def to_json(self):
        return {
            'id_location': self.id_location,
            'name': self.name,
            'address': self.address,
            'department': self.department,
            'schedule': self.schedule,
            'price_range': self.price_range,
            'phone': self.phone,
            'id_user': self.id_user
        }