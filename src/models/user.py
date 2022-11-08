from init import db, ma
from marshmallow import fields

class User(db.Model):
    '''Create a user model'''
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)

    customers = db.relationship('Customer', back_populates='user', cascade='all, delete')

class UserSchema(ma.Schema):
    customers = fields.List(fields.Nested('CustomerSchema', only=['id', 'phone']))

    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email','password', 'is_admin', 'customers')
        ordered = True # Display data in the order as listed in the fields above