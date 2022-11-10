from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Regexp, OneOf, And, Length
from marshmallow.exceptions import ValidationError

class Postcode(db.Model):
    ''' Create postcode model'''

    __tablename__ = 'postcodes'
    
    postcode = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(100), nullable=False)

    addresses = db.relationship('Address', back_populates='postcode')


class PostcodeSchema(ma.Schema):
    postcode = fields.Integer(strict=True, required=True)
    
    @validates('state')
    def validate_state(self, value):
        try:
            value = float(value)
            raise ValidationError('You have to enter characters in the state.')
        except ValueError:
            if any(letter.isdigit() for letter in value):
                raise ValidationError('State must not contain numbers.')



    class Meta:
        fields = ('postcode','state')
        ordered = True # Display data in the order as listed in the fields above
        
        