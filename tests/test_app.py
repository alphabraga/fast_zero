from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user(client):
    user = {
        'username': 'alfredo',
        'password': '491901',
        'email': 'alphabraga@hotmail.com',
    }

    response = client.post('/user', json=user)

    assert response.status_code == HTTPStatus.CREATED
    # userAssert = {'username': 'alphabraga', 'email': 'alphabraga@hotmail.com'}
    assert response.json()


def test_list_user(client):
    response = client.get('/users')

    users = response.json()

    assert response.status_code == HTTPStatus.OK
    assert isinstance(users, dict)


def test_update_user(client):
    user = {
        'username': 'aaaaa',
        'password': '491901',
        'email': 'aaaaa@hotmail.com',
    }

    response = client.post('/user', json=user)

    saved_user = response.json()

    username = saved_user.get('username')

    assert username == 'aaaaa'

    saved_user['username'] = 'alfredo'

    id = int(saved_user.get('id'))

    response = client.put(f'/user/{id}', json=saved_user)

    updated_user = response.json()

    assert updated_user.get('username') == 'alfredo'
