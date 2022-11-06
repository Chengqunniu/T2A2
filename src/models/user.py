from init import db, ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class UserSchema(ma.Schema):
    customers = fields.List(fields.Nested('CustomerSchema', exclude=['user']))

    class Meta:
        fields = ('id', 'first_name', 'last_name', 'password', 'is_admin')
        