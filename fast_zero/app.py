from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_zero.schemas import (
    Message,
    UserCreate,
    UserDB,
    UserPublic,
    UsersPublic,
)

app = FastAPI(
    title='Fast Zero',
    summary='Um sistema do curso fast zero',
    version='1.0.2',
    contact='suporte@emap.ma.gov.br',
)

database = [
    {
        'id': 1,
        'username': 'um',
        'email': 'um@example.com',
        'password': '111111',
    },
    {
        'id': 2,
        'username': 'dois',
        'email': 'dois@example.com',
        'password': '111111',
    },
    {
        'id': 3,
        'username': 'tres',
        'email': 'tres@example.com',
        'password': '111111',
    },
    {
        'id': 4,
        'username': 'quatro',
        'email': 'quatro@example.com',
        'password': '111111',
    },
    {
        'id': 5,
        'username': 'cinco',
        'email': 'cinco@example.com',
        'password': '111111',
    },
]


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    message = Message
    message.message = 'Olá Mundo!'

    return message


@app.get('/users', status_code=HTTPStatus.OK, tags=['usuarios'])
def list_users():
    users = UsersPublic(users=database)

    return users


@app.post(
    '/user',
    status_code=HTTPStatus.CREATED,
    response_model=UserPublic,
    tags=['usuarios'],
)
def create_user(user: UserCreate):
    """Cadastrar um usuario"""
    auto_increment_id = len(database) + 1
    userDB = UserDB(**user.model_dump(), id=auto_increment_id)
    database.append(userDB)

    return userDB


@app.get(
    '/user/{id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
    tags=['usuarios'],
)
def get_user(id: int):
    try:
        data = database[id - 1]
        return data
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'user with {id} not found',
        )


@app.put(
    '/user/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
    tags=['usuarios'],
)
def update_user(user_id: int, user: UserPublic):
    try:
        database[user_id - 1]
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'user with {user_id} not found',
        )

    database[user_id - 1] = user
    return UserPublic(**user.model_dump())


@app.delete(
    '/users/{id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
    tags=['usuarios'],
)
def delete(id: int):
    database[id] = None
