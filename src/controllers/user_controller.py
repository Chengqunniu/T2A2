from flask import Blueprint, request, abort
from init import db, bcrypt
from datetime import timedelta
from models.user import User, UserSchema
from models.customer import Customer, CustomerSchema
from models.address import Address, AddressSchema
from models.postcode import Postcode, PostcodeSchema
from models.payment_account import PaymentAccount, PaymentAccountSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/')
@jwt_required()
def get_all_users():
    '''Get information about all users'''
    # authorize()
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude=['password']).dump(users)

@user_bp.route('/<int:user_id>/')
@jwt_required()
def get_single_user(user_id):
    '''Get information about a specific user'''
    # authorize()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    # If user with user_id exists, return its information
    # If not exists, return error message
    if user:
        return UserSchema(exclude=['password']).dump(user)
    else:
        return {'error': f'user not found with id {user_id}'}, 404


@user_bp.route('/update/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_user():
    ''' Update information about a specific user'''

    data = UserSchema().load(request.json)

    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    if 'first_name' in data.keys():
        user.first_name = data['first_name'] or user.first_name
    if 'last_name' in data.keys():
        user.last_name = data['last_name'] or user.last_name
    if 'password' in data.keys():
        if data['password'] is None:
            user.password = user.password
        else:
            user.password = bcrypt.generate_password_hash(data['password']).decode('utf8')
    if 'email' in data.keys():
        user.email = data['email'] or user.email

    db.session.commit()

    return UserSchema().dump(user)


@user_bp.route('/<int:user_id>/', methods=['DELETE'])
@jwt_required()
def delete_one_user(user_id):
    ''' Delete sepecific user'''
    authorize()  # Only allow admin to delete users

    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
        db.session.delete(user)
        db.session.commit()
        return {'message': f"User '{user.first_name} {user.last_name}' deleted successfully"}
    else:
        return {'error': f'User not found with id {id}'}, 404


@user_bp.route('/register/', methods=['POST'])
def user_register():
    ''' Register new user'''
    # Error handling if email already registered
    data = UserSchema().load(request.json)

    try:
    # Create a new User model instance
    # Request.json returns decode json to dict
        user = User(
            first_name = data['first_name'],
            last_name = data['last_name'],
            password = bcrypt.generate_password_hash(data['password']).decode('utf8'),
            email = data['email']
        )
    # Add and commit user to DB
        db.session.add(user)
        db.session.commit()
    # Response back to the client, user marshmallow to serialize data
        return UserSchema(exclude=['password']).dump(user), 201
    except IntegrityError:
        return {'error': 'Email address already in use'}, 409


@user_bp.route('/login/', methods=['POST'])
def user_login():
    ''' Login the user'''

    # First check whether user exist
    stmt = db.select(User).filter_by(email=request.json['email'])
    user = db.session.scalar(stmt)
    # Check wheter user matach the password
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        # If login successfully, create a token for the user
        # Return token, users' info to the client
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return {'email': user.email, 'token': token, 'is_admin': user.is_admin}, 200
    else:
        # If login fails, tell the client either email or password is invalid
        # Not telling the client specifically which is wrong
        # Otherwise, hackers will notice one of them is valid and attack on the other
        return {'error': 'Invalid email or password'}, 401 


@user_bp.route('/customer/', methods=['POST'])
@jwt_required()
def customer_register():
    ''' Register new customer'''

    data = CustomerSchema().load(request.json)

    # Error handling if phone number already registered
    try:
    # Create a new Customer model instance
    # Request.json returns decode json to dict
        customer = Customer(
            phone = data['phone'],
            user_id = get_jwt_identity(),
            address_id = data['address_id']
        )
    # Add and commit user to DB
        db.session.add(customer)
        db.session.commit()
    # Response back to the client, user marshmallow to serialize data
        return CustomerSchema(exclude='address_id').dump(customer), 201
    except IntegrityError:
        return {'error': 'Address id does not exists'}, 409
    

@user_bp.route('/customer/')
@jwt_required()
def get_all_customers():
    '''Get information about all customers'''
    stmt = db.select(Customer)
    customers = db.session.scalars(stmt)
    return CustomerSchema(many=True, exclude='address_id').dump(customers)


@user_bp.route('/customer/<int:customer_id>/')
def get_single_customer(customer_id):
    '''Get information abobut a specific customer'''
    # authorize()
    stmt = db.select(Customer).filter_by(id=customer_id)
    customer = db.session.scalar(stmt)
    # If user with customer_id exists, return its information
    # If not exists, return error message
    if customer:
        return CustomerSchema(exclude='address_id').dump(customer)
    else:
        return {'error': f'user not found with id {customer_id}'}, 404


@user_bp.route('/customer/update/phone', methods=['PUT', 'PATCH'])
@jwt_required()
def update_customer_phone():
    ''' Update phone about a specific customer'''

    data = CustomerSchema().load(request.json)


    user_id = get_jwt_identity()
    
    stmt = db.select(Customer).filter_by(user_id=user_id)
    customer = db.session.scalar(stmt)

    customer.phone = data['phone'] or customer.phone

 
    db.session.commit()

    return CustomerSchema(exclude='address_id').dump(customer)

@user_bp.route('/customer/update/address', methods=['PUT', 'PATCH'])
@jwt_required()
def update_customer_address():
    ''' Update address about a specific customer'''

    user_id = get_jwt_identity()
    
    stmt = db.select(Customer).filter_by(user_id=user_id)
    customer = db.session.scalar(stmt)

    customer.address_id = check_address()
 
    db.session.commit()

    return CustomerSchema(exclude='address_id').dump(customer)

@user_bp.route('/customer/address/')
@jwt_required()
def get_all_addresses():
    '''Get information about all addresses'''
    stmt = db.select(Address)
    addresses = db.session.scalars(stmt)
    return AddressSchema(many=True).dump(addresses)

@user_bp.route('/customer/address/<int:address_id>/')
def get_single_address(address_id):
    '''Get information abobut a specific address'''
    # authorize()
    stmt = db.select(Address).filter_by(id=address_id)
    address = db.session.scalar(stmt)
    # If user with address_id exists, return its information
    # If not exists, return error message
    if address:
        return AddressSchema().dump(address)
    else:
        return {'error': f'user not found with id {address_id}'}, 404

@user_bp.route('/customer/address/postcode/')
@jwt_required()
def get_all_postcodes():
    '''Get information about all postcodes'''
    stmt = db.select(Postcode)
    postcodes = db.session.scalars(stmt)
    return PostcodeSchema(many=True).dump(postcodes)

@user_bp.route('/customer/address/postcode/<int:postcode_id>/')
def get_single_postcode(postcode_id):
    '''Get information abobut a specific postcode'''
    # authorize()
    stmt = db.select(Postcode).filter_by(postcode=postcode_id)
    postcode = db.session.scalar(stmt)
    # If user with postcode_id exists, return its information
    # If not exists, return error message
    if postcode:
        return PostcodeSchema().dump(postcode)
    else:
        return {'error': f'user not found with id {postcode_id}'}, 404

@user_bp.route('/customer/address/postcode/', methods=['POST'])
@jwt_required()
def create_postcode():
    '''Create single postcode each time'''

    data = PostcodeSchema().load(request.json)
    try:
        postcode = Postcode(
            postcode = data['postcode'],
            state = data['state']
            )

        db.session.add(postcode)
        db.session.commit()
        return PostcodeSchema().dump(postcode)
    except IntegrityError:
        return {'error': f'Postcode {postcode.postcode} already exists.'}


@user_bp.route('/customer/payment_account/')
@jwt_required()
def get_all_payment_accounts():
    '''Get information about all payment_accounts'''
    user_id = get_jwt_identity()
    
    stmt = db.select(Customer).filter_by(user_id=user_id)
    customer = db.session.scalar(stmt)

    stmt = db.select(PaymentAccount).filter_by(customer_id=customer.id)
    payment_accounts = db.session.scalars(stmt)
    return PaymentAccountSchema(many=True, exclude='card_no').dump(payment_accounts)

@user_bp.route('/customer/payment_account/<int:payment_account_id>')
@jwt_required()
def get_single_payment_account(payment_account_id):
    '''Get information abobut a specific postcode'''

    user_id = get_jwt_identity()
    
    stmt = db.select(Customer).filter_by(user_id=user_id)
    customer = db.session.scalar(stmt)
    stmt = db.select(PaymentAccount).filter_by(id=payment_account_id, customer_id=customer.id)
    payment_account = db.session.scalar(stmt)
    # If user with postcode_id exists, return its information
    # If not exists, return error message
    if payment_account:
        return PaymentAccountSchema(exclude='card_no').dump(payment_account)
    else:
        return {'error': f'Payment Account not found with id {payment_account_id}'}, 404


@user_bp.route('/customer/payment_account/', methods=['POST'])
@jwt_required()
def create_payment_account():
    ''' Create new payment_account'''
    # Create a new PaymentAccount model instance
    # Request.json returns decode json to dict
    data = PaymentAccountSchema().load(request.json)

    user_id = get_jwt_identity()
    
    stmt = db.select(Customer).filter_by(user_id=user_id)
    customer = db.session.scalar(stmt)
    try:
        payment_account = PaymentAccount(
            owner_name = data['owner_name'],
            expire_date = data['expire_date'],
            card_no = data['card_no'],
            security_no = data['security_no'],
            encrypted_card_no = PaymentAccount.encrypt_card_no(data['card_no']),
            customer_id = customer.id 
        )
        # Add and commit payment_account to DB
        db.session.add(payment_account)
        db.session.commit()
        # Response back to the client, user marshmallow to serialize data
        return PaymentAccountSchema(exclude='card_no').dump(payment_account), 201
    except IntegrityError:
        return {'error': f'Card number already exists.'}
        

@user_bp.route('/customer/payment_account/<int:payment_account_id>/', methods=['DELETE'])
@jwt_required()
def delete_one_payment_account(payment_account_id):
    ''' Delete sepecific payment account'''
    # authorize()  # Only allow admin to delete users
    user_id = get_jwt_identity()
    
    stmt = db.select(Customer).filter_by(user_id=user_id)
    customer = db.session.scalar(stmt)

    stmt = db.select(PaymentAccount).filter_by(id=payment_account_id, customer_id=customer.id)
    payment_account = db.session.scalar(stmt)
    if payment_account:
        db.session.delete(payment_account)
        db.session.commit()
        return {'message': f"Customer with id {customer.id}'s payment account with id {payment_account_id} deleted successfully"}
    else:
        return {'error': f'Customer with id {customer.id} does not have payment account with id {payment_account_id}'}, 404


def authorize():
    ''' Authorize user'''
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if not user.is_admin:
        abort(401)

def check_address():
    ''' Check whether address is already in the database
    If exists, assign the address_id to the customer
    instead of creating the same address again
    If not exists, create new address and assign the
    address_id to the customer'''

    data = AddressSchema().load(request.json)

    stmt = db.select(Address).filter_by(street_number=data['street_number'], street_name=data['street_name'],
    suburb=data['suburb'], postcode_id=data['postcode_id'])
    address = db.session.scalar(stmt)
    if address is None:  # Check whether the address already exists
            
            # Create a new Address model instance
            # Request.json returns decode json to dict
            address = Address(
            street_number = data['street_number'],
            street_name = data['street_name'],
            suburb = data['suburb'],
            postcode_id = data['postcode_id']
            )
            # Add and commit user to DB
            db.session.add(address)
            db.session.commit()
    
            # Response back to the client, user marshmallow to serialize data
            # return AddressSchema().dump(address), 201
        
    return address.id



