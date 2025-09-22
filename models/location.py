from config.db import db
import uuid

class Location(db.Model):
    __tablename__ = 'locations'

    id_location = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    schedule = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, name, address, department, schedule, phone):
        self.name = name
        self.address = address
        self.department = department
        self.schedule = schedule
        self.phone = phone

    def to_json(self):
        return {
            'id_location': self.id_location,
            'name': self.name,
            'address': self.address,
            'department': self.department,
            'schedule': self.schedule,
            'phone': self.phone
        }