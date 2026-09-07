from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_recommendations_valid_user():
    response = client.get("/recommendations/U101")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "U101"
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0
    assert "score" in data["items"][0]
    assert "product_id" in data["items"][0]


def test_get_recommendations_empty_user_id():
    # FastAPI treats "/recommendations/ " with a space as a valid path param;
    # this checks our explicit empty-string validation logic.
    response = client.get("/recommendations/%20")
    assert response.status_code == 400


def test_recommendations_are_cached_on_second_call():
    user_id = "U202"
    first = client.get(f"/recommendations/{user_id}")
    second = client.get(f"/recommendations/{user_id}")

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["cached"] is False
    assert second.json()["cached"] is True
    assert first.json()["items"] == second.json()["items"]


def test_response_schema_shape():
    response = client.get("/recommendations/U303")
    data = response.json()
    assert set(data.keys()) == {"user_id", "items", "cached"}
    for item in data["items"]:
        assert set(item.keys()) == {"product_id", "score"}
