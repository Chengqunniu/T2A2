from init import db, ma
from marshmallow import fields

class OrderDetail(db.Model):
    ''' Create order_detail model'''

    __tablename__ = 'order_details'
    
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)

    order = db.relationship('Order', back_populates='order_details')
    product = db.relationship('Product', back_populates='order_details')



class OrderDetailSchema(ma.Schema):
    ''' Schema for OrderDetail'''
    
    product = fields.Nested('ProductSchema', only=['id', 'name'])
    order = fields.Nested('OrderSchema', only=['id'])
    # Validate price entered, make sure it is a number
    price = fields.Integer(strict=True, required=True)
    # Validate quantity entered, make sure it is a number
    quantity = fields.Integer(strict=True, required=True)
    # Validate order_id entered, make sure it is a number
    order_id = fields.Integer(strict=True)
    # Validate product_id entered, make sure it is a number
    product_id = fields.Integer(strict=True)


    class Meta:
        fields = ('id', 'price', 'quantity', 'product', 'order', 'order_id', 'product_id')
        ordered = True # Display data in the order as listed in the fields above
        