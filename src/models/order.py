from init import db, ma
from marshmallow import fields

ORDER_STATUS_ID =[1,2]

class Order(db.Model):
    ''' Create order model'''

    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.Date, nullable=False)
    ship_date = db.Column(db.String, default='Not shipped', nullable=False)
    order_status_id = db.Column(db.Integer, db.ForeignKey("order_statues.id"), default=ORDER_STATUS_ID[0], nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    shipping_method_id = db.Column(db.Integer, db.ForeignKey("shipping_methods.id"), nullable=False)

    order_status = db.relationship('OrderStatus', back_populates='orders')
    customer = db.relationship('Customer', back_populates='orders')
    shipping_method = db.relationship('ShippingMethod', back_populates='orders')
    order_details = db.relationship('OrderDetail', back_populates='order', cascade='all, delete')



class OrderSchema(ma.Schema):
    user = fields.List(fields.Nested('UserSchema', only=['id']))
    address = fields.List(fields.Nested('AddressSchema', exclude=['customers']))
    shipping_method = fields.Nested('ShippingMethodSchema', exclude=['id'])
    order_details = fields.List(fields.Nested('OrderDetailSchema'))
    order_status = fields.Nested('OrderStatusSchema', exclude=['id'])

    order_date = fields.Date(strict=True)
    ship_date = fields.String(strict=True)
    order_status_id = fields.Integer(strict=True, load_default=ORDER_STATUS_ID[0])
    customer_id = fields.Integer(strict=True)
    shipping_method_id = fields.Integer(strict=True, required=True)



    
    class Meta:
        fields = ('id', 'order_date', 'ship_date', 'order_status', 'order_status_id', 'customer_id', 'shipping_method_id','shipping_method','order_details')
        ordered = True # Display data in the order as listed in the fields above
    