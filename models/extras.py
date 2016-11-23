from models.databaseInit import db

class Extra(db.Model):
    __tablename__ = 'extras'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String, nullable=False)
    hireStart = db.Column(db.Date, nullable=True)
    hireEnd = db.Column(db.Date, nullable=True)

    bookingId = db.Column(db.Integer, db.ForeignKey('bookings.id'))

    def __init__(self, extraType, bookingId, hireStart=None, hireEnd=None):
        self.type = extraType
        self.hireStart = hireStart
        self.hireEnd = hireEnd
        self.bookingId = bookingId

    def __repr__(self):
        return '<Guest Name N: %r>' % self.type

