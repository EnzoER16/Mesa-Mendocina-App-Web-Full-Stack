import io

def test_full_flow(test_client):
    # -------- Registro --------
    res = test_client.post("/users/auth/register", data={
        "username": "enzo",
        "email": "enzo@test.com",
        "password": "1234",
        "role": "owner"   # necesario para crear location
    }, follow_redirects=True)

    assert res.status_code == 200

    # -------- Login --------
    res = test_client.post("/users/auth/login", data={
        "email": "enzo@test.com",
        "password": "1234",
    }, follow_redirects=True)

    assert res.status_code == 200

    # -------- Crear Local --------
    fake_image = (io.BytesIO(b"fakeimage"), "test.jpg")

    res = test_client.post("/locations/create", data={
        "name": "Mi Local",
        "address": "Calle falsa",
        "department": "Capital",
        "phone": "123456",
        "description": "Local de prueba",
        "image": fake_image
    }, content_type="multipart/form-data", follow_redirects=True)

    assert res.status_code == 200

    # -------- Verificar que aparece en /locations/ --------
    res = test_client.get("/locations/")
    assert b"Mi Local" in res.data