from init import db, ma
from marshmallow import fields

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Text, nullable=False)

    products = db.relationship('Product', back_populates='category')



class CategorySchema(ma.Schema):

    class Meta:
        fields = ('id', 'type')
        