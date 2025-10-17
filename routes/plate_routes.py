from flask import Blueprint, jsonify, request
from config.db import db
from models.plate import Plate
from models.location import Location
from routes.user_routes import token_required
