from init import db, ma
from marshmallow import fields

class OrderStatus(db.Model):
    __tablename__ = 'order_status'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)

    orders = db.relationship('Order', back_populates='status')


class OrderStatusSchema(ma.Schema):

    class Meta:
        fields = ('postcode','state')
        