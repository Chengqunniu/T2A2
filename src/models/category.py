from init import db, ma
from marshmallow import fields, validates
from marshmallow.exceptions import ValidationError


class Category(db.Model):
    ''' Create category model'''

    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Text, nullable=False, unique=True)

    products = db.relationship('Product', back_populates='category')



class CategorySchema(ma.Schema):
    ''' Schema for category'''

    type = fields.String(strict=True)

    @validates('type')
    def validate_type(self, value):
        try:
            value = float(value)
            raise ValidationError('You have to enter characters for the product name.')
        except ValueError:
            if any(letter.isdigit() for letter in value):
                raise ValidationError('Product name must not contain numbers.')
            else:
                stmt = db.select(db.func.count()).select_from(Category).filter_by(type=value)
                count = db.session.scalar(stmt)
                if count > 0:
                    raise ValidationError('Category type has already been used')

    class Meta:
        fields = ('id', 'type')
        ordered = True # Display data in the order as listed in the fields above
        