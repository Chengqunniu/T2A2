from init import db, ma
from marshmallow import fields

class ShippingMethod(db.Model):
    __tablename__ = 'shipping_methods'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    orders = db.relationship('Order', back_populates='shipping_method')


class ShippingMethodSchema(ma.Schema):

    class Meta:
        fields = ('id', 'type', 'price')
        