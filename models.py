from app import db
from flask_login import UserMixin

class Item(db.Model):
    __tablename__ = 'items'

    pid = db.Column(db.Integer, primary_key=True)
    invRef = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    condition = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text(32))
    image = db.Column(db.String(255), default='static/img/no_picture.png', nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)  # Link to the User model

    user = db.relationship('User', backref='items', lazy=True)  # Relationship to access item's creator

    def __repr__(self):
        return f'Title:{self.title},  asking price: {self.price}'
    
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False) # Hashed later

    def __repr__(self):
        return f'Username:{self.username}'
    
    def get_id(self):
        return self.uid