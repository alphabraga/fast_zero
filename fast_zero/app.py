from http import HTTPStatus

from fastapi import FastAPI

from fast_zero.schemas import (
    Message,
    UserDB,
    UserPublic,
    UserSchema,
    UsersPublic,
)

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    message = Message
    message.message = 'Olá Mundo!'

    return message


@app.get('/users', status_code=HTTPStatus.OK, response_model=UsersPublic)
def list_users():
    return {'users': database}


@app.post('/user', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    auto_increment_id = len(database) + 1

    userDB = UserDB(**user.model_dump(), id=auto_increment_id)

    database.append(userDB)

    return user
