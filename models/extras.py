from models.databaseInit import db
from datetime import datetime


def addAllExtrasByBookingId(extras, bookingId):
    extrasList = []
    for key, value in extras.items():
        if value or value == {}:
            print(key, "   ", value)
            if key == 'carHire':
                extrasList.append(Extra(
                    key,
                    bookingId,
                    datetime.strptime(value['hireStart'], '%Y-%m-%d'),
                    datetime.strptime(value['hireEnd'], '%Y-%m-%d')))
            else:
                extrasList.append(Extra(key, bookingId))
    return extrasList


def deleteAllExtrasByBookingId(bookingId):
    Extra.query.filter_by(bookingId=bookingId).delete()
    db.session.commit()


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

