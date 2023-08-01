from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):

    new_user = User(
        username='alice', password='123456', email='alice@hotmail.com'
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user.username == 'alice'
