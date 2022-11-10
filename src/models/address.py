from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Regexp, OneOf, And
from marshmallow.exceptions import ValidationError


class Address(db.Model):
    '''Create address model'''
    __tablename__ = 'addresses'
    
    id = db.Column(db.Integer, primary_key=True)
    street_number = db.Column(db.Integer, nullable=False)
    street_name = db.Column(db.String(100), nullable=False)
    suburb = db.Column(db.String(100), nullable=False)
    postcode_id = db.Column(db.Integer, db.ForeignKey("postcodes.postcode"), nullable=False)
  
    customers = db.relationship('Customer', back_populates='address')
    postcode = db.relationship('Postcode', back_populates='addresses')

class AddressSchema(ma.Schema):
    ''' Schema for address'''

    postcode = fields.Nested('PostcodeSchema')
    street_number = fields.Integer(strict=True, required=True)
    postcode_id = fields.Integer(strict=True, required=True)
 

    @validates('street_name')
    def validate_street_name(self, value):
        try:
            value = float(value)
            raise ValidationError('You have to enter characters in the street name.')
        except ValueError:
            if any(letter.isdigit() for letter in value):
                raise ValidationError('Street_name must not contain numbers.')

    @validates('suburb')
    def validate_suburb(self, value):
        try:
            value = float(value)
            raise ValidationError('You have to enter characters in the street name.')
        except ValueError:
            if any(letter.isdigit() for letter in value):
                raise ValidationError('Street_name must not contain numbers.')



    class Meta:
        fields = ('id','street_number', 'street_name', 'suburb','postcode_id', 'postcode')
        ordered = True # Display data in the order as listed in the fields above

        