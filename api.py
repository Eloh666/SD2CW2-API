from authentication.authenticateUser import authenticate, identity
from controllers import bookingController
from flask import Flask
from flask_jwt import JWT
from flask_restful import Api
from models.database import db
from models.users import User




# App setup
app = Flask(__name__)
app.config['DEBUG'] = True

# Initialises DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///static/db/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)
db.app = app
with app.app_context():
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





if __name__ == '__main__':
    app.run(debug=True)
