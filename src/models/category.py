from init import db, ma
from marshmallow import fields, validates
from marshmallow.exceptions import ValidationError


class Category(db.Model):
    ''' Create category model'''

    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Text, nullable=False, unique=True)

    products = db.relationship('Product', back_populates='category')


class CategorySchema(ma.Schema):
    ''' Schema for category'''
    
    products = fields.List(fields.Nested('ProductSchema', only=['name', 'price']))

    # Validate category type entered, make sure it is a string
    type = fields.String(strict=True)

    @validates('type')
    def validate_type(self, value):
        ''' Validate category type'''
        # Raise an exception if category type is a number or includes number in it
        try:
            value = float(value)
            raise ValidationError('You have to enter characters for the product name.')
        except ValueError:
            if any(letter.isdigit() for letter in value):
                raise ValidationError('Product name must not contain numbers.')


    class Meta:
        fields = ('id', 'type', 'products')
        ordered = True # Display data in the order as listed in the fields above
        