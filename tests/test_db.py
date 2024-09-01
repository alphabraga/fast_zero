from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(username='aaaa22', email='aaa22@aaa.com', password='aaaaa')
    session.add(user)
    session.commit()
    result = session.scalar(select(User).where(User.email == 'aaa22@aaa.com'))

    assert result.username == 'aaaa22'
