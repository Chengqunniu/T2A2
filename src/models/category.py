from init import db, ma

class Category(db.Model):
    ''' Create category model'''

    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Text, nullable=False, unique=True)

    products = db.relationship('Product', back_populates='category')



class CategorySchema(ma.Schema):
    ''' Schema for category'''

    class Meta:
        fields = ('id', 'type')
        