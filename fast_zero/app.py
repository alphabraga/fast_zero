from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import (
    Message,
    UserCreate,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI(
    title='Fast Zero', summary='Um sistema do curso fast zero', version='1.0.2'
)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    message = Message
    message.message = 'Olá Mundo!'

    return message


@app.get(
    '/users',
    status_code=HTTPStatus.OK,
    response_model=UserList,
    tags=['usuarios'],
)
def list_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@app.post(
    '/user',
    status_code=HTTPStatus.CREATED,
    response_model=UserPublic,
    tags=['usuarios'],
)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    """Cadastrar um usuario"""
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                detail='Ja existe username', status_code=HTTPStatus.BAD_REQUEST
            )

        elif db_user.email == user.email:
            raise HTTPException(
                detail='Ja existe email', status_code=HTTPStatus.BAD_REQUEST
            )

    user_db = User(**user.model_dump())

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db


@app.get(
    '/user/{id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
    tags=['usuarios'],
)
def get_user(id: int):
    try:
        data = [][id - 1]
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
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'User with user id {user_id} not found',
        )

    db_user.username = user.username
    db_user.password = user.password
    db_user.email = user.email
    session.commit()
    session.refresh(db_user)

    return db_user


@app.delete(
    '/user/{id}',
    status_code=HTTPStatus.OK,
    tags=['usuarios'],
)
def delete(id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'User with user id {id} not found',
        )

    session.delete(db_user)
    session.commit()

    message = Message(message=f'User with id {id} deleted with success')

    return message
