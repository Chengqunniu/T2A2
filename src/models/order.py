from init import db, ma
from marshmallow import fields

ORDER_STATUS_ID =[1,2]  # List of status, used for validation

class Order(db.Model):
    ''' Create order model'''

    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.Date, nullable=False)
    ship_date = db.Column(db.String, default='Not shipped', nullable=False)
    order_status_id = db.Column(db.Integer, db.ForeignKey("order_statues.id"), 
    default=ORDER_STATUS_ID[0], nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    shipping_method_id = db.Column(db.Integer, db.ForeignKey("shipping_methods.id"), nullable=False)

    order_status = db.relationship('OrderStatus', back_populates='orders')
    customer = db.relationship('Customer', back_populates='orders')
    shipping_method = db.relationship('ShippingMethod', back_populates='orders')
    order_details = db.relationship('OrderDetail', back_populates='order', cascade='all, delete')



class OrderSchema(ma.Schema):
    ''' Schema for Order'''
    
    customer = fields.Nested('CustomerSchema', only=['id', 'phone', 'address'])
    shipping_method = fields.Nested('ShippingMethodSchema', exclude=['id'])
    order_details = fields.List(fields.Nested('OrderDetailSchema'))
    order_status = fields.Nested('OrderStatusSchema', exclude=['id'])

    # Validate order_date entered, make sure it is a date type
    order_date = fields.Date(strict=True)
    # Validate ship_date entered, make sure it is a string
    ship_date = fields.String(strict=True)
    # Validate order_status_id entered, make sure it is a number
    # Set default to 1
    order_status_id = fields.Integer(strict=True, load_default=ORDER_STATUS_ID[0])
    # Validate customer_id entered, make sure it is a number
    customer_id = fields.Integer(strict=True)
    # Validate shipping_method_id entered, make sure it is a number
    shipping_method_id = fields.Integer(strict=True, required=True)


    class Meta:
        fields = ('id', 'order_date', 'ship_date', 'order_status', 'order_status_id', 'customer_id', 
        'shipping_method_id','shipping_method','order_details', 'customer')
        ordered = True # Display data in the order as listed in the fields above
    