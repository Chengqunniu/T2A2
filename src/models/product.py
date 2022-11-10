from init import db, ma
from marshmallow import fields, validates
from marshmallow.exceptions import ValidationError


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

    description = fields.String(strict=True)
    price = fields.Float(strict=True, required=True)
    stock = fields.Integer(strict=True, required=True)
    create_date = fields.Date(strict=True)
    category_id = fields.Integer(strict=True)

    @validates('name')
    def validate_name(self, value):
        try:
            value = float(value)
            raise ValidationError('You have to enter characters for the product name.')
        except ValueError:
            if any(letter.isdigit() for letter in value):
                raise ValidationError('Product name must not contain numbers.')
            else:
                stmt = db.select(db.func.count()).select_from(Product).filter_by(name=value)
                count = db.session.scalar(stmt)
                if count > 0:
                    raise ValidationError('Product name has already been used')




    class Meta:
        fields = ('id', 'name', 'description', 'price', 'stock', 'create_date', 'category', 'category_id')
        ordered = True # Display data in the order as listed in the fields above
        
        