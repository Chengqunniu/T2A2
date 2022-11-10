from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Regexp, OneOf, And, Length
from marshmallow.exceptions import ValidationError

IS_ADMIN = [True, False]

class User(db.Model):
    '''Create a user model'''
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=IS_ADMIN[1])

    customers = db.relationship('Customer', back_populates='user', cascade='all, delete')

class UserSchema(ma.Schema):
    customers = fields.List(fields.Nested('CustomerSchema', only=['id', 'phone']))
    
    password = fields.String(strict=True, validate=And(
        Length(min=8, error='Password must be at least 8 characters'),
        Regexp('^[a-zA-Z0-9]+$', error='Only letters, numbers are allowed.')
    ))

    email = fields.Email(required=True, strict=True)
    is_admin = fields.Boolean(load_default=IS_ADMIN[1], validate=
        OneOf(IS_ADMIN), error='is_admin must be True or False.')

    @validates('first_name')
    def validate_first_name(self, value):
        try:
            value = float(value)
            raise ValidationError('You have to enter characters in the first_name.')
        except ValueError:
            if any(letter.isdigit() for letter in value):
                raise ValidationError('First_name must not contain numbers.')

    @validates('last_name')
    def validate_last_name(self, value):
        try:
            value = float(value)
            raise ValidationError('You have to enter characters in the last_name.')
        except ValueError:
            if any(letter.isdigit() for letter in value):
                raise ValidationError('Last_name must not contain numbers.')





    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email','password', 'is_admin', 'customers')
        ordered = True # Display data in the order as listed in the fields above