from models.user import User
from config.db import db

def test_user_model_creation(test_client):
    user = User(username="enzo", email="enzo@test.com", password="1234")

    db.session.add(user)
    db.session.commit()

    assert user.id_user is not None
    assert user.username == "enzo"
    assert user.check_password("1234") is True