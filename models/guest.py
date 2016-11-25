from models.databaseInit import db


def addAllGuestsByBookingId(guests, bookingId):
    guestsList = []
    for guest in guests:
        guestsList.append(Guest(
            guest['name'],
            guest['age'],
            guest['passport'],
            bookingId))
    return guestsList


def deleteAllGuestsByBookingId(bookingId):
    Guest.query.filter_by(bookingId=bookingId).delete()
    db.session.commit()


class Guest(db.Model):
    __tablename__ = 'guests'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    passportNumber = db.Column(db.String, nullable=False)

    bookingId = db.Column(db.Integer, db.ForeignKey('bookings.id'))

    def __init__(self, name, age, passportNumber, bookingId):
        self.name = name
        self.age = age
        self.passportNumber = passportNumber
        self.bookingId = bookingId

    def __repr__(self):
        return '<Guest Name N: %r>' % self.name
