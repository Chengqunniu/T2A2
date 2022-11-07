from init import db, ma
from marshmallow import fields

class PaymentAccount(db.Model):
    __tablename__ = 'payment_accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    card_no = db.Column(db.Integer, nullable=False)
    owner_name = db.Column(db.String(100), nullable=False)
    expire_date = db.Column(db.String, nullable=False)
    security_no = db.Column(db.Integer, nullable=False)
    encrypted_card_no = db.Column(db.String(100), nullable=False)


    customer = db.relationship('Customer', back_populates='payment_accounts')
    orders = db.relationship('PaymentAccount', back_populates='payment_account')

    @staticmethod
    def encrypt_card_no(number):
        '''Only display the first and last part of the card to protect customers condifidential information'''
        new_card_no = str(number)[:4] + str('*' * 8) + str(number)[-4:]

        return new_card_no

class PaymentAccountSchema(ma.Schema):


    class Meta:
        fields = ('id', 'encrypted_card_no', 'owner_name', 'expire_date', 'security_no')
        