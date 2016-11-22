from models.databaseInit import db


class Extra(db.Model):
    __tablename__ = 'extras'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String, nullable=False)
    arrivalDate = db.Column(db.Date, nullable=False)
    departureDate = db.Column(db.Date, nullable=False)

    bookingId = db.Column(db.Integer, db.ForeignKey('bookings.id'))

    def __init__(self, name, address, age, passportNumber):
        self.name = name
        self.address = address
        self.age = age
        self.passportNumber = passportNumber

    def __repr__(self):
        return '<Guest Name N: %r>' % self.name

