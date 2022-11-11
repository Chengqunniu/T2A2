from init import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf

# List of ratings used for validation
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
    ''' Schema for review'''

    # Validate rating entered, make sure it is a number
    # Make sure it is from 1 to 5
    rating = fields.Integer(strict=True, required=True, validate=
        OneOf(VALID_RATINGS, error='Only numbers 1 to 5')
    )
    # Validate comment entered, make sure it is a string
    comment = fields.String(strict=True, required=True)
    # Validate customer_id entered, make sure it is a number
    customer_id = fields.Integer(strict=True)
    # Validate product_id entered, make sure it is a number
    product_id = fields.Integer(strict=True)
    
    
    class Meta:
        fields = ('id', 'comment', 'rating', 'customer_id', 'product_id')
        ordered = True # Display data in the order as listed in the fields above
        
        