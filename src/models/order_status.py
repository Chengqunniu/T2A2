from init import db, ma
from marshmallow import validates
from marshmallow.exceptions import ValidationError

class OrderStatus(db.Model):
    ''' Create order_status model'''

    __tablename__ = 'order_statues'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), unique=True, nullable=False)

    orders = db.relationship('Order', back_populates='order_status')


class OrderStatusSchema(ma.Schema):
    ''' Schema for OrderStatus'''

    @validates('type')
    def validate_type(self, value):
        ''' Validate the order status type entered''' 
        # Raise an exception if the type is a number or includes number in it
        try:
            value = float(value)
            raise ValidationError('You have to enter characters for the type.')
        except ValueError:
            if any(letter.isdigit() for letter in value):
                raise ValidationError('Type must not contain numbers.')

                
    class Meta:
        fields = ('id', 'type')
        ordered = True # Display data in the order as listed in the fields above
        
        