from fastapi.testclient import TestClient

from fast_zero.app import app

client = TestClient(app)


def test_root_deve_retornar_200_e_ola_mundo():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Olá Mundo!'}


def test_one_plus_one():
    assert 1 + 1 == 2


def test_read_users():
    response = client.get('/users')

    assert response.status_code == 200

    assert response.json()


def test_create_user():
    response = client.post(
        '/users',
        json={
            'email': 'alphabraga@hotmail.com',
            'username': 'alphabraga',
            'password': '123456',
        },
    )

    assert response.status_code == 201


def test_update_user_must_return_404():
    response = client.put(
        '/usuers/0',
        json={
            'email': 'alphabraga@hotmail.com',
            'username': 'alphabraga',
            'password': '123456',
        },
    )

    assert response.status_code == 404


def test_update_user():

    response = client.post(
        '/users',
        json={
            'email': 'alphabraga@hotmail.com',
            'username': 'alphabraga',
            'password': '123456',
        },
    )

    assert response.status_code == 201
    user = response.json()
    new_id = user.get('id')
    assert new_id == 2

    response = client.put(
        f'/users/{new_id}',
        json={
            'email': 'alphabragaUPDATED@hotmail.com',
            'username': 'alphabragaUPDATED',
            'password': '123456',
        },
    )

    assert response.status_code == 201
    assert response.json().get('username') == 'alphabragaUPDATED'


def test_remove_user():

    response = client.delete('/users/1')
    assert response.status_code == 200
