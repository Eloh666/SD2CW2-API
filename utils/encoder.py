import bcrypt


def encode(password):
    salt = bcrypt.gensalt()
    combo_password = password.encode('utf-8') + 'NapierHoldays'.encode('utf-8')
    return bcrypt.hashpw(combo_password, salt)
