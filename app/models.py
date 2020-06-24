from app import login
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User(str(id))


class User(UserMixin):
    def __init__(self, username):
        self.username = username

    def is_authenticated(self):
        return True

    @property
    def id(self):
        return self.username
