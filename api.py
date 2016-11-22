from authentication.authenticateUser import authenticate, identity
from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from models.databaseInit import db

from controllers import bookingController
from controllers import customerController



# App setup
app = Flask(__name__)
app.config['DEBUG'] = True

# Initialises DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///static/db/bookingDatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)
db.app = app
with app.app_context():

    # imports model to init the database
    from models.usersModel import User
    from models.customers import Customer
    from models.bookings import Booking
    from models.guest import Guest
    from models.extras import Extra

    db.create_all()


if not User.query.filter_by(username='Eloh666').first():
    admin = User('Eloh666', 'holidayVillage')
    db.session.add(admin)
    db.session.commit()

# Initialises secury Settings
app.config['SECRET_KEY'] = 'super-secret'
jwt = JWT(app, authenticate, identity)



# Setup app as restful API
api = Api(app)

# APIs routes
api.add_resource(bookingController.BookingController, '/booking')
api.add_resource(customerController.CustomerController, '/customer')





if __name__ == '__main__':
    app.run(debug=True)
