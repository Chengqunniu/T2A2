from init import db, ma
from marshmallow import fields

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.Integer, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    address_id = db.Column(db.Integer, db.ForeignKey("addresses.id"))

    user = db.relationship('User', back_populates='customers')
    address = db.relationship('Address', back_populates='customers')
    payment_accounts = db.relationship('PaymentAccount', back_populates='customer', cascade='all, delete')
    orders = db.relationship('Order', back_populates='customer', cascade='all, delete')
    reviews = db.relationship('Review', back_populates='customer', cascade='all, delete')



class CustomerSchema(ma.Schema):
    address = fields.Nested('AddressSchema')
    user = fields.Nested('UserSchema', only=['id', 'first_name', 'last_name'])

    payment_accounts = fields.List(fields.Nested('PaymentAccountSchema', only=['encrypted_card_no']))
    orders = fields.List(fields.Nested('OrderSchema', exclude=['payment_account', 'customer_id']))
    reviews = fields.List(fields.Nested('ReviewSchema', exclude=['customer_id']))


    class Meta:
        fields = ('id', 'phone', 'address', 'user')
        ordered = True
        