from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from fast_zero.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user(client):
    user = {
        'username': 'alphabraga',
        'password': '491901',
        'email': 'alphabraga@hotmail.com',
    }

    response = client.post('/user', json=user)

    assert response.status_code == HTTPStatus.CREATED
    userAssert = {'username': 'alphabraga', 'email': 'alphabraga@hotmail.com'}
    assert response.json() == userAssert


def test_list_user(client):
    response = client.get('/users')

    users = response.json()

    assert response.status_code == HTTPStatus.OK
    assert isinstance(users, dict)
