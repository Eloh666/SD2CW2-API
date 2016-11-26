from models.databaseInit import db


def alc2json(row):
    return dict([(col, str(getattr(row,col))) for col in row.__table__.columns.keys()])


def serializeBooking(booking):
    guests = [alc2json(guest) for guest in booking.guests]
    myDict = {
        'Id': str(booking.id),
        'ArrivalDate': str(booking.arrivalDate),
        'DepartureDate': str(booking.departureDate),
        'CustomerId': booking.customerId,
        'DietaryReqs': booking.dietaryReqs,
        'Guests': guests,
    }
    for k in [alc2json(extra) for extra in booking.extras]:
        if not k['type'] == 'carHire':
            del k['hireStart']
            del k['hireEnd']
        myDict[k['type']] = k
    return myDict

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    arrivalDate = db.Column(db.Date, nullable=False)
    departureDate = db.Column(db.Date, nullable=False)

    dietaryReqs = db.Column(db.String, nullable=True)

    customerId = db.Column(db.Integer, db.ForeignKey('customers.referenceNumber'))

    guests = db.relationship("Guest")
    extras = db.relationship("Extra")

    def __init__(self, arrival, departure, customerId):
        self.arrivalDate = arrival
        self.departureDate = departure
        self.customerId = customerId

    def __repr__(self):
        return '<Booking N: %r>' % self.id
