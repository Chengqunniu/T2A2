from init import db, ma
from marshmallow import fields, validates
from marshmallow.exceptions import ValidationError

class Customer(db.Model):
    ''' Create customer model'''

    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.Integer, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    address_id = db.Column(db.Integer, db.ForeignKey("addresses.id"))

    user = db.relationship('User', back_populates='customer')
    address = db.relationship('Address', back_populates='customers')
    payment_accounts = db.relationship('PaymentAccount', back_populates='customer', cascade='all, delete')
    orders = db.relationship('Order', back_populates='customer', cascade='all, delete')
    reviews = db.relationship('Review', back_populates='customer', cascade='all, delete')



class CustomerSchema(ma.Schema):
    ''' Schema for customer'''

    address = fields.Nested('AddressSchema')
    payment_accounts = fields.List(fields.Nested('PaymentAccountSchema', only=['encrypted_card_no']))
    orders = fields.List(fields.Nested('OrderSchema', exclude=['payment_account', 'customer_id']))
    reviews = fields.List(fields.Nested('ReviewSchema', exclude=['customer_id']))
    user = fields.Nested('UserSchema', only=['id', 'first_name', 'last_name'])

    # Validate phone number entered, make sure it is a number
    phone = fields.Integer(strict=True, required=True)
    # Validate address id entered, make sure it is a number
    address_id = fields.Integer(strict=True)
    # Validate user_id entered, make sure it is a number
    user_id = fields.Integer(strict=True, required=True)


    @validates('phone')
    def validate_phone(self, value):
        ''' Validate the phone number entered, make sure it is unique'''
        stmt = db.select(db.func.count()).select_from(Customer).filter_by(phone=value)
        count = db.session.scalar(stmt)
        if count > 0:
            raise ValidationError('Phone number has already been used')

    class Meta:
        fields = ('id', 'phone', 'address', 'user', 'address_id')
        ordered = True # Display data in the order as listed in the fields above

        