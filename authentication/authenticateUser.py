from werkzeug.security import safe_str_cmp
from models.usersModel import User
from utils.encoder import encodePassword


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and safe_str_cmp(user.password, encodePassword(password)):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.query.filter_by(id=user_id).first()
