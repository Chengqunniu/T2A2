from flask import Blueprint, request, abort
from init import db, bcrypt
from datetime import timedelta
from models.user import User, UserSchema
from models.customer import Customer, CustomerSchema
from models.address import Address, AddressSchema
from models.postcode import Postcode, PostcodeSchema
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
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    user.first_name = request.json.get('first_name') or user.first_name
    user.last_name = request.json.get('last_name') or user.last_name
    if request.json.get('password') == None:
        user.password = user.password
    else:
        user.password = bcrypt.generate_password_hash(request.json.get('password')).decode('utf8')
    user.email = request.json.get('email') or user.email

    db.session.commit()

    return UserSchema().dump(user)


@user_bp.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_one_user(id):
    ''' Delete sepecific user'''
    authorize()  # Only allow admin to delete users

    stmt = db.select(User).filter_by(id=id)
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
    try:
    # Create a new User model instance
    # Request.json returns decode json to dict
        user = User(
            first_name = request.json['first_name'],
            last_name = request.json['last_name'],
            password = bcrypt.generate_password_hash(request.json['password']).decode('utf8'),
            email = request.json['email']
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
    # Error handling if phone number already registered
    try:
    # Create a new Customer model instance
    # Request.json returns decode json to dict
        customer = Customer(
            phone = request.json['phone'],
            user_id = get_jwt_identity()
        )
    # Add and commit user to DB
        db.session.add(customer)
        db.session.commit()
    # Response back to the client, user marshmallow to serialize data
        return CustomerSchema().dump(customer), 201
    except IntegrityError:
        return {'error': 'Customer already exists'}, 409
    
@user_bp.route('/customer/', methods=['GET'])
@jwt_required()
def get_all_customers():
    '''Get information about all customers'''
    stmt = db.select(Customer)
    customers = db.session.scalars(stmt)
    return CustomerSchema(many=True).dump(customers)

@user_bp.route('/customer/<int:customer_id>/')
def get_single_customer(customer_id):
    '''Get information abobut a specific customer'''
    # authorize()
    stmt = db.select(Customer).filter_by(id=customer_id)
    customer = db.session.scalar(stmt)
    # If user with customer_id exists, return its information
    # If not exists, return error message
    if customer:
        return CustomerSchema().dump(customer)
    else:
        return {'error': f'user not found with id {customer_id}'}, 404


@user_bp.route('/customer/update/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_customer():
    ''' Update information about a specific customer'''


    user_id = get_jwt_identity()
    
    stmt = db.select(Customer).filter_by(user_id=user_id)
    customer = db.session.scalar(stmt)


    customer.phone = request.json.get('phone') or customer.phone


    data = CustomerSchema().load(request.json)
    
    if 'address'in data.keys():
        new_address = data['address']
        stmt = db.select(Address).filter_by(street_number=new_address['street_number'], street_name=new_address['street_name'],
        suburb=new_address['suburb'])
        address = db.session.scalar(stmt)
        if address is None:  # Check whether the address already exists
            
            # Create a new postcode 
            postcode = Postcode(
            postcode= (new_address['postcode'])['postcode'],
            state = (new_address['postcode'])['state']
            )

            db.session.add(postcode)
            db.session.commit()
            

            # Create a new Address model instance
            # Request.json returns decode json to dict
            address = Address(
            street_number = new_address['street_number'],
            street_name = new_address['street_name'],
            suburb = new_address['suburb'],
            postcode_id = (new_address['postcode'])['postcode']
            )


            # Add and commit user to DB
            db.session.add(address)
            db.session.commit()
    
            # Response back to the client, user marshmallow to serialize data
            # return AddressSchema().dump(address), 201
        
        customer.address_id = address.id
    else:
        customer.address_id = customer.address_id


    db.session.commit()

    return CustomerSchema().dump(customer)

@user_bp.route('/customer/address/', methods=['GET'])
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

@user_bp.route('/customer/address/postcode/', methods=['GET'])
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


# @user_bp.route('/customer/update/address/', methods=['POST'])
# @jwt_required()
# def update_customer_address():
    # ''' Update customer's address'''

#     try:
#     # Create a new Address model instance
#     # Request.json returns decode json to dict
#         address = Address(
#             street_number = data['street_number'],
#             street_name = data['street_name'],
#             suburb = data['suburb'],
#             postcode_id= data['postcode_id']
#         )
#     # Add and commit user to DB
#         db.session.add(address)
#         db.session.commit()
        
        
#         # suburb=data['suburb'], postcode_id=data['postcode_id'])
#         # address = db.session.scalar(stmt)
#         # address_id = address.id

#         # user_id = get_jwt_identity()
    
#         # stmt = db.select(Customer).filter_by(user_id=user_id)
#         # customer = db.session.scalar(stmt)
#         # customer.address_id = address_id

#     # Response back to the client, user marshmallow to serialize data
#         return AddressSchema().dump(address), 201
#     except IntegrityError:
#         return {'error': 'Customer already exists'}, 409


    



def authorize():
    ''' Authorize user'''
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if not user.is_admin:
        abort(401)