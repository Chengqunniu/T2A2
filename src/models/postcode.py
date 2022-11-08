from init import db, ma
from marshmallow import fields

class Postcode(db.Model):
    __tablename__ = 'postcodes'
    
    postcode = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(100), nullable=False)

    addresses = db.relationship('Address', back_populates='postcode')


class PostcodeSchema(ma.Schema):

    class Meta:
        fields = ('postcode','state')
        