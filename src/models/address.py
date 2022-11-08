from init import db, ma
from marshmallow import fields

class Address(db.Model):
    __tablename__ = 'addresses'
    
    id = db.Column(db.Integer, primary_key=True)
    street_number = db.Column(db.Integer, nullable=False)
    street_name = db.Column(db.String(100), nullable=False)
    suburb = db.Column(db.String(100), nullable=False)
    postcode_id = db.Column(db.Integer, db.ForeignKey("postcodes.postcode"), nullable=False)
  
    customers = db.relationship('Customer', back_populates='address')
    postcode = db.relationship('Postcode', back_populates='addresses')

class AddressSchema(ma.Schema):
    postcode = fields.Nested('PostcodeSchema')


    class Meta:
        fields = ('id','street_number', 'street_name', 'suburb','postcode_id', 'postcode')
        ordered = True
        