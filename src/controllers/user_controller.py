from flask import Blueprint, request, abort
from init import db, bcrypt
from datetime import timedelta
from models.user import User, UserSchema
from models.customer import Customer, CustomerSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


user_bp = Blueprint('auth', __name__, url_prefix='/user')

@user_bp.route('/')
def get_all_users():
    '''Get information about all users'''
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude=['password']).dump(users)

@user_bp.route('/<int:user_id>/')
def get_single_user(user_id):
    '''Get information about all users'''
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    # If user with user_id exists, return its information
    # If not exists, return error message
    if user:
        return UserSchema(exclude=['password']).dump(user)
    else:
        return {'error': f'user not found with id {user_id}'}, 404

@user_bp.route('/register/', methods=['POST'])
def user_register():
    ''' Register new user'''
    # Error handling if email already registered
    try:
    # Create a new User model instance from the user_info
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
    # Create a new User model instance from the user_info
    # Request.json returns decode json to dict
        customer = Customer(
            phone = request.json['phone'],
            user_id = get_jwt_identity()
        )
    # Add and commit user to DB
        db.session.add(customer)
        db.session.commit()
    # Response back to the client, user marshmallow to serialize data
        return CustomerSchema(exclude=['password']).dump(customer), 201
    except IntegrityError:
        return {'error': 'Phone number already in use'}, 409

def authorize():
    ''' Authorize user'''
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if not user.is_admin:
        abort(401)