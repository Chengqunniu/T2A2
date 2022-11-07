from flask import Blueprint
from init import db
# from models.customer import Customer
from models.payment_account import PaymentAccount, PaymentAccountSchema
# from models.user import User


db_commands = Blueprint('db', __name__)


@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print("Tables created")

@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command('seed')
def seed_db():
    # users = [
    #     User(
    #         email='admin@spam.com',
    #         password=bcrypt.generate_password_hash('eggs').decode('utf-8'),#originally hashing return hexadecimal, it is better to use utf8
    #         is_admin=True
    #     ),
    #     User(
    #         name='John Cleese',
    #         email='someone@spam.com',
    #         password=bcrypt.generate_password_hash('12345').decode('utf-8')
    #     )
    # ]
    payment_accounts = [
        PaymentAccount(
            card_no = 1234567890,
            owner_name = 'John Cleese',
            expire_date = '12/01/2022',
            security_no = 500,
            encrypted_card_no = PaymentAccount.encrypt_card_no(1234567890)
        )
    ]
    db.session.add_all(payment_accounts)
    db.session.commit()

@db_commands.route('/')
def get_all_payment_accounts():
    stmt = db.select(PaymentAccount)
    payment_account = db.session.scalar(stmt)
    return PaymentAccountSchema().dump(payment_account)