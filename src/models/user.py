from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Regexp, OneOf, And, Length
from marshmallow.exceptions import ValidationError


# List of boolean value for this field, used for validation
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

    customer = db.relationship('Customer', back_populates='user', cascade='all, delete')

class UserSchema(ma.Schema):
    ''' Schema for user'''

    customer = fields.List(fields.Nested('CustomerSchema', only=['id', 'phone']))
    
    # Validate password entered, make sure it is a string
    # Make sure the password is at least 8 characters
    # Includes letters, numbers only
    password = fields.String(strict=True, validate=And(
        Length(min=8, error='Password must be at least 8 characters'),
        Regexp('^[a-zA-Z0-9]+$', error='Only letters, numbers are allowed.')
    ))
    # Validate email entered, make sure it is a Email type
    email = fields.Email(required=True, strict=True)
    # Validate is_admin value entered, make sure it is a boolean value
    # Must be one of the value in the list
    is_admin = fields.Boolean(load_default=IS_ADMIN[1], validate=
        OneOf(IS_ADMIN), error='is_admin must be True or False.')

    @validates('first_name')
    def validate_first_name(self, value):
        ''' Validate the first_name entered'''
        # Raise an exception if the first_name is a number or includes number in it
        try:
            value = float(value)
            raise ValidationError('You have to enter characters in the first_name.')
        except ValueError:
            if any(letter.isdigit() for letter in value):
                raise ValidationError('First_name must not contain numbers.')


    @validates('last_name')
    def validate_last_name(self, value):
        ''' Validate the last_name entered'''
        # Raise an exception if the last_name is a number or includes number in it
        try:
            value = float(value)
            raise ValidationError('You have to enter characters in the last_name.')
        except ValueError:
            if any(letter.isdigit() for letter in value):
                raise ValidationError('Last_name must not contain numbers.')


    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email','password', 'is_admin', 'customer')
        ordered = True # Display data in the order as listed in the fields above