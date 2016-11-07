from models.databaseInit import db


class Guest(db.Model):
    __tablename__ = 'guests'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    passportNumber = db.Column(db.String, nullable=False)

    bookingId = db.Column(db.Integer, db.ForeignKey('bookings.id'))

    def __init__(self, name, address, age, passportNumber):
        self.name = name
        self.address = address
        self.age = age
        self.passportNumber = passportNumber

    def __repr__(self):
        return '<Guest Name N: %r>' % self.name

