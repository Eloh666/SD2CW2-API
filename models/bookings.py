from models.databaseInit import db


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    arrivalDate = db.Column(db.Date, nullable=False)
    departureDate = db.Column(db.Date, nullable=False)
    customerId = db.Column(db.Integer, db.ForeignKey('customers.referenceNumber'))

    bookings = db.relationship("Guest")

    def __init__(self, arrival, departure, customerId):
        self.arrivalDate = arrival
        self.departureDate = departure
        self.customerId = customerId

    def __repr__(self):
        return '<Booking N: %r>' % self.id
