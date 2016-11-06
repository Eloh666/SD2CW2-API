from flask_restful import abort
from functools import wraps
from flask_jwt import current_identity
from werkzeug.security import safe_str_cmp
from models.users import User
from utils.encoder import encodePassword


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and safe_str_cmp(user.password, encodePassword(password)):
        return user


def checkUser(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_identity.username == 'user1':
            return func(*args, **kwargs)
        return abort(401)
    return wrapper
