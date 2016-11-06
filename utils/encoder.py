import hashlib

def encodePassword(password):
    salt = "mySuperSecretSalt".encode('utf-8')
    combo_password = password.encode('utf-8') + 'NapierHoldays'.encode('utf-8') + salt
    return hashlib.md5(combo_password).hexdigest()
