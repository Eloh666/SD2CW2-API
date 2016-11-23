from models.databaseInit import db


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
