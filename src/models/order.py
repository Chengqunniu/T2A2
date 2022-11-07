from init import db, ma
from marshmallow import fields

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.Date, nullable=False)
    ship_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Integer, db.ForeignKey("order_status.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    shipping_method = db.Column(db.Integer, db.ForeignKey("shipping_methods.id"), nullable=False)
    payment_account = db.Column(db.Integer, db.ForeignKey("payment_accounts.id"), nullable=False)

    status = db.relationship('Status', back_populates='orders')
    customer = db.relationship('Customer', back_populates='orders')
    shipping_method = db.relationship('ShippingMethod', back_populates='orders')
    payment_account = db.relationship('PaymentAccount', back_populates='orders')



class OrderSchema(ma.Schema):
    user = fields.List(fields.Nested('UserSchema', only=['id']))
    address = fields.List(fields.Nested('AddressSchema', exclude=['customers']))
    payment_account = fields.List(fields.Nested('PaymentMethodSchema', only=['encrypted_card_no']))
    shipping_method = fields.List(fields.Nested('ShippingMethodSchema', exclude=['id']))


    class Meta:
        fields = ('id', 'order_date', 'ship_date', 'status', 'customer_id', 'shipping_method', 'payment_account')
        