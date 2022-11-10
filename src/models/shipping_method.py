from init import db, ma
from marshmallow import fields, validates
from marshmallow.exceptions import ValidationError


class ShippingMethod(db.Model):
    ''' Create shipping_Method model'''

    __tablename__ = 'shipping_methods'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Text, nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)

    orders = db.relationship('Order', back_populates='shipping_method')


class ShippingMethodSchema(ma.Schema):
    price = fields.Float(strict=True, required=True)

    @validates('type')
    def validate_type(self, value):
        try:
            value = float(value)
            raise ValidationError('You have to enter characters for the type.')
        except ValueError:
            if any(letter.isdigit() for letter in value):
                raise ValidationError('Type must not contain numbers.')


    class Meta:
        fields = ('id', 'type', 'price')
        ordered = True
        