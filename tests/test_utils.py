from flask import Blueprint
from utils.authentication import login_required

def test_password_hashing():
    from werkzeug.security import generate_password_hash, check_password_hash

    password = "1234"
    hashed = generate_password_hash(password)

    assert hashed != password
    assert check_password_hash(hashed, "1234") is True