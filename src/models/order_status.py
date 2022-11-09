from init import db, ma
from marshmallow import fields

class OrderStatus(db.Model):
    ''' Create order_status model'''

    __tablename__ = 'order_statues'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), unique=True, nullable=False)

    orders = db.relationship('Order', back_populates='order_status')


class OrderStatusSchema(ma.Schema):

    class Meta:
        fields = ('id', 'type')
        