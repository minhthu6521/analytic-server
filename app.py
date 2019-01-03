from Analytics import create_app
app = create_app('../config.py')

import mock
from models.user_model import User
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa

base = declarative_base()
engine = sa.create_engine('mysql://root:salasana@localhost/Analytics?charset=utf8mb4')
base.metadata.bind = engine
session = orm.scoped_session(orm.sessionmaker())(bind=engine)

user = session.query(User).filter_by(email="analytics@example.com").first()
if user:
    user.is_authenticated = True


@mock.patch('flask_login.utils._get_user', return_value=user)
def run_app():
    app.run()


if __name__ == "__main__":
    run_app()