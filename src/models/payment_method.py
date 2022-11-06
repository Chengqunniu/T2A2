from init import db, ma
from marshmallow import fields

class PaymentMethod(db.Model):
    __tablename__ = 'payment_methods'
    
    id = db.Column(db.Integer, primary_key=True)
    card_no = db.Column(db.Integer, nullable=False)
    owner_name = db.Column(db.String(100), nullable=False)
    expire_date = db.Column(db.Date, nullable=False)
    security_no = db.Column(db.Integer(3), nullable=False)

    customer = db.relationship('Customer', back_populates='payment_methods')


class PaymentMethodSchema(ma.Schema):
    # customers = fields.List(fields.Nested('CustomerSchema', exclude=['user', 'card']))


    class Meta:
        fields = ('id','card_no', 'owner_name', 'expire_date', 'security_no')
        