from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# tests of endpoint /imports

# у категорий поле price должно содержать null
def test_category_price_null():

    response = client.post("/imports", json={"items": [ { "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "name": "string", "parentid": "3fa85f64-5717-4562-b3fc-2c963f66afa1", "type": "CATEGORY", "price": None } ], "updateDate": "2022-06-29T19:49:33.480Z"})
    assert response.status_code == 201

    response = client.post("/imports", json={"items": [ { "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "name": "string", "parentid": "3fa85f64-5717-4562-b3fc-2c963f66afa1", "type": "CATEGORY", "price": 1 } ], "updateDate": "2022-06-29T19:49:33.480Z"})
    assert response.status_code == 400


# цена товара не может быть null и должна быть больше либо равна нулю.
def test_offer_price():

    response = client.post("/imports", json={"items": [ { "id": "3fa85f64-5717-4562-b3fc-2c963f66afa2", "name": "string", "parentid": "3fa85f64-5717-4562-b3fc-2c963f66afa1", "type": "OFFER", "price": 10 } ], "updateDate": "2022-06-29T19:49:33.480Z"})
    assert response.status_code == 201

    response = client.post("/imports", json={"items": [ { "id": "3fa85f64-5717-4562-b3fc-2c963f66afa2", "name": "string", "parentid": "3fa85f64-5717-4562-b3fc-2c963f66afa1", "type": "OFFER", "price": None } ], "updateDate": "2022-06-29T19:49:33.480Z"})
    assert response.status_code == 400


# в одном запросе не может быть двух элементов с одинаковым id
def test_unique_id():
    response = client.post("/imports", json={"items": [ { "id": "3fa85f64-5717-4562-b3fc-2c963f66afa2", "name": "string", "parentid": "3fa85f64-5717-4562-b3fc-2c963f66afa1", "type": "OFFER", "price": None },{ "id": "3fa85f64-5717-4562-b3fc-2c963f66afa2", "name": "string", "parentid": "3fa85f64-5717-4562-b3fc-2c963f66afa1", "type": "OFFER", "price": None } ], "updateDate": "2022-06-29T19:49:33.480Z"})
    assert response.status_code == 400

# дата должна обрабатываться согласно ISO 8601 (такой придерживается OpenAPI). Если дата не удовлетворяет данному формату, необходимо отвечать 400.
def test_isodate():
    response = client.post("/imports", json={"items": [ { "id": "3fa85f64-5717-4562-b3fc-2c963f66afa2", "name": "string", "parentid": "3fa85f64-5717-4562-b3fc-2c963f66afa1", "type": "OFFER", "price": None } ], "updateDate": "2022-06-29T19:49:33"})
    assert response.status_code == 400