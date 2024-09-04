from http import HTTPStatus

# from fast_zero.schemas import UserPublic


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


def test_list_user_with_no_users(client):
    response = client.get('/users')

    users = response.json()

    assert response.status_code == HTTPStatus.OK
    assert users == {'users': []}


def test_list_user_with_user(client, user):
    response = client.get('/users')
    users = response.json()
    assert response.status_code == HTTPStatus.OK
    assert len(users['users']) >= 1


def test_update_user_dont_exists(client):
    user = {
        'id': 999,
        'username': 'aaaaa',
        'password': '491901',
        'email': 'aaaaa@hotmail.com',
    }

    not_exists_id = 999

    response = client.put(f'/user/{not_exists_id}', json=user)

    assert response.status_code == HTTPStatus.NOT_FOUND


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
    saved_user['password'] = '491901'
    saved_user['email'] = 'aaaaa@hotmail.com'

    id = int(saved_user.get('id'))

    response = client.put(f'/user/{id}', json=saved_user)

    response.status_code == HTTPStatus.OK

    updated_user = response.json()

    assert updated_user['username'] == 'alfredo'


def test_delete_user_not_exists(client):
    response = client.delete('/user/9999')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client, user):
    response = client.delete(f'/user/{user.id}')
    assert response.status_code == HTTPStatus.OK
