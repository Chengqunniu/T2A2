from init import db, ma
from marshmallow import fields

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.Integer, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey("addresses.id"))

    user = db.relationship('User', back_populates='customers')
    address = db.relationship('Address', back_populates='customers')
    payment_accounts = db.relationship('PaymentAccount', back_populates='customer', cascade='all, delete')
    orders = db.relationship('Order', back_populates='customer', cascade='all, delete')
    reviews = db.relationship('Review', back_populates='customer')



class CustomerSchema(ma.Schema):
    user = fields.List(fields.Nested('UserSchema', only=['id']))
    address = fields.List(fields.Nested('AddressSchema', exclude=['customers']))
    payment_accounts = fields.List(fields.Nested('PaymentAccountSchema', only=['encrypted_card_no']))
    orders = fields.List(fields.Nested('OrderSchema', exclude=['payment_account', 'customer_id']))
    reviews = fields.List(fields.Nested('ReviewSchema', exclude=['customer_id']))


    class Meta:
        fields = ('id', 'phone', 'address', 'user', 'payment_accounts', 'orders', 'reviews')
        