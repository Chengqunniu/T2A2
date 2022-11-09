from init import db, ma
from marshmallow import fields

class Product(db.Model):
    ''' Create product model'''

    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    create_date = db.Column(db.Date, nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

    category = db.relationship('Category', back_populates='products')
    order_details = db.relationship('OrderDetail', back_populates='product')
    reviews = db.relationship('Review', back_populates='product', cascade='all, delete')




class ProductSchema(ma.Schema):
    category = fields.Nested('CategorySchema', only=['type'])
    reviews = fields.List(fields.Nested('ReviewSchema', exclude=['product_id']))

    
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'stock', 'create_date', 'category')
        ordered = True
        