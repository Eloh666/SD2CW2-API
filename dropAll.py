from api import db

if __name__ == '__main__':
    db.drop_all()
    db.session.commit()