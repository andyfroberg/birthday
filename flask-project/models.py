from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
loginManager=LoginManager()

##CREATE TABLE
class UserModel(UserMixin, db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    passwordHash = db.Column(db.String(128), nullable=False)
    events = db.relationship('EventModel', backref='user_model')
    
    def setPassword(self, password):
        self.passwordHash = generate_password_hash(password)
    
    def checkPassword(self, password):
        return check_password_hash(self.passwordHash, password)
    
    def __repr__(self):
        return f'<User "{self.username}"'
    
class EventModel(UserMixin, db.Model):
    event_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    event_title = db.Column(db.String(50), nullable=False)
    event_date = db.Column(db.Integer, nullable=False)
    user_owner = db.Column(db.Integer, db.ForeignKey('user_model.id'))

    def __repr__(self):
        return f'<Event "{self.event_title}"'

@loginManager.user_loader
def loadUser(id):
    return UserModel.query.get(int(id))