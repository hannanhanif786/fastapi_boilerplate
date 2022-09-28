import json
from urllib import request, response
from urllib.request import Request
from fastapi.testclient import TestClient
import sys
import os
import pytest
from fastapi import Request

# FOR PARENT DIRECTORY PATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app


client = TestClient(app)


@pytest.fixture
def token_headers():
    """Used for authentication endpoint

    Returns:
        _type_: return token for authenticated endpoint
    """

    data = {"username": "hannan.hanif@txend.com", "password": "string"}
    response = client.post("/login", data=data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_update_user():
    """Test case for updated user"""
    data = {"name": "Hannan", "phone_no": "030000"}
    response = client.put("/user/3", json.dumps(data))
    assert response.status_code == 200


def test_delete_user():
    """Test case for deleted user"""
    response = client.delete("/user/16")
    assert response.status_code == 200


def test_retrieve_item_by_id():
    """Test case for retrieve user"""
    response = client.get("/user/8")
    assert response.status_code == 200
    assert response.json() == {
        "name": "Hannan1",
        "email": "hannan1@example.com",
        "phone_no": "030000",
    }


def test_create_user(token_headers):
    """testcase for add new user

    Args:
        token_headers (_type_): _description_
    """
    data = {
        "name": "Ali",
        "email": "ali54321@example.com",
        "password": "54321",
        "phone_no": "03001234567",
    }
    head = token_headers
    response = client.post("/user/", json.dumps(data), headers=head)
    assert response.status_code == 200


def test_change_password(token_headers):
    data = {
        "old_password": "string",
        "new_password": "54321",
        "confirm_password": "54321",
    }
    head = token_headers
    response = client.post("/change-password", json.dumps(data), headers=head)
    assert response.status_code == 200


def test_reset_password():
    data = {
        "email": "hannan.hanif@txend.com",
    }
    response = client.post("/reset-password", json.dumps(data), Request)
    assert response.status_code == 200
