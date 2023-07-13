from django.test import TestCase


def test_healthcheck_ok(client):
    response = client.get("/healthcheck/")
    assert response.status_code == 200
    assert response.content == b"OK"
