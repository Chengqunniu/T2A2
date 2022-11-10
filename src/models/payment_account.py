from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Range, Length
from marshmallow.exceptions import ValidationError

class PaymentAccount(db.Model):
    ''' Create payment account model'''

    __tablename__ = 'payment_accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    card_no = db.Column(db.String, nullable=False, unique=True)
    owner_name = db.Column(db.String(100), nullable=False)
    expire_date = db.Column(db.String, nullable=False)
    security_no = db.Column(db.Integer, nullable=False)
    encrypted_card_no = db.Column(db.String(100), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)

    customer = db.relationship('Customer', back_populates='payment_accounts')


    @staticmethod
    def encrypt_card_no(number):
        '''Only display the first and last part of the card to protect customers condifidential information'''
        new_card_no = (number[:4]) + str('*' * 8) + (number[-4:])

        return new_card_no

class PaymentAccountSchema(ma.Schema):

    card_no = fields.String(strict=True, required=True, validate=
        Length(equal=16, error='card_no must be 16 digits long.'))
    expire_date = fields.String(strict=True, required=True)
    security_no = fields.Integer(strict=True, required=True, validate=
        Range(min=3,max=3, error='security_no must be 3 digits long.'))
    
    @validates('owner_name')
    def validate_owner_name(self, value):
        try:
            value = float(value)
            raise ValidationError('You have to enter characters in the owner_name.')
        except ValueError:
            if any(letter.isdigit() for letter in value):
                raise ValidationError('Owner_name must not contain numbers.')

    class Meta:
        fields = ('id', 'encrypted_card_no', 'owner_name', 'expire_date', 'security_no', 'customer_id', 'card_no')
        ordered = True # Display data in the order as listed in the fields above
        