from models.databaseInit import db


def serializeCustomer(customer):
    return {
        'ReferenceNumber': customer.referenceNumber,
        'Name': customer.name,
        'Address': customer.address
    }


class Customer(db.Model):
    __tablename__ = 'customers'
    referenceNumber = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    bookings = db.relationship("Booking")

    def __init__(self, name, address):
        self.name = name
        self.address = address

    def __repr__(self):
        return '<Customer Name N: %r>' % self.name
