from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp


VALID_RATINGS = (1, 2, 3, 4, 5)

class Review(db.Model):
    ''' Create review model'''

    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)

    customer = db.relationship('Customer', back_populates='reviews')
    product = db.relationship('Product', back_populates='reviews')



class ReviewSchema(ma.Schema):
    rating = fields.Integer(validate=Regexp('^[1-5]+$', error='Only numbers 1 to 5'))
    
    class Meta:
        fields = ('id', 'comment', 'rating', 'customer_id', 'product_id')
        