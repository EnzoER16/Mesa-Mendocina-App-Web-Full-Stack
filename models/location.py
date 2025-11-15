from config.db import db
import uuid

class Location(db.Model):
    __tablename__ = 'locations'

    id_location = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(200), nullable=True, default="no_image.png")

    id_user = db.Column(db.String(36), db.ForeignKey("users.id_user"), nullable=False)
    
    plates = db.relationship("Plate", backref="location", lazy=True)
    ratings = db.relationship("Rating", backref="location", lazy=True)
    reservations = db.relationship("Reservation", backref="location", lazy=True)

    def __init__(self, name, address, department, phone, id_user, description=None, image="no_image.png"):
        self.name = name
        self.address = address
        self.department = department
        self.phone = phone
        self.id_user = id_user
        self.description = description
        self.image = image

    def to_json(self):
        return {
            'id_location': self.id_location,
            'name': self.name,
            'address': self.address,
            'department': self.department,
            'phone': self.phone,
            'description': self.description,
            'image': self.image,
            'id_user': self.id_user
        }