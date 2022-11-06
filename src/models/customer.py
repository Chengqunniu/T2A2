from init import db, ma
from marshmallow import fields

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.Integer, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    address = db.Column(db.Integer, db.ForeignKey("addresses.id"), nullable=False)

    user = db.relationship('User', back_populates='customers', cascade='all, delete')
    address = db.relationship('Address', back_populates='customers')
    payment_methods = db.relationship('PaymentMethod', back_populates='customer')


class CustomerSchema(ma.Schema):
    user = fields.List(fields.Nested('UserSchema', only=['id']))
    address = fields.List(fields.Nested('AddressSchema', exclude=['customers']))
    payment_methods = fields.List(fields.Nested('PaymentMethodSchema', exclude=['customer']))

    class Meta:
        fields = ('id', 'email', 'phone', 'address', 'user', 'paymeent_methods')
        