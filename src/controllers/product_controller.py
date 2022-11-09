from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required
from models.product import Product, ProductSchema
from models.category import Category, CategorySchema
from models.review import Review, ReviewSchema
from sqlalchemy.exc import IntegrityError
from datetime import date

    
product_bp = Blueprint('product', __name__, url_prefix='/product')

@product_bp.route('/')
@jwt_required()
def get_all_product():
    '''Get information about all products'''
    stmt = db.select(Product)
    products = db.session.scalars(stmt)
    return ProductSchema(many=True).dump(products) 


@product_bp.route('/<int:product_id>/')
@jwt_required()
def get_single_product(product_id):
    '''Get information about a specific product'''
    stmt = db.select(Product).filter_by(id=product_id)
    product = db.session.scalar(stmt)
    if product:
        return ProductSchema().dump(product) 
    else:
        return {'error': f'Product not found with id {product_id}'}, 404

@product_bp.route('/', methods=['POST'])
@jwt_required()
def create_products():
    '''Create new products, only allowed for admin'''
    # authorize()
    try:
        # Create a new Product Method model instance
        # Request.json returns decode json to dict
        product = Product(
            name = request.json['name'],
            description = request.json['description'],
            price = request.json['price'],
            stock = request.json['stock'],
            category_id = request.json['category_id'],
            create_date = date.today()
            )

        db.session.add(product)
        db.session.commit()

        # Response back to the client, user marshmallow to serialize data
        return ProductSchema().dump(product), 201

    except IntegrityError:
        return {'error': 'Product name already exists'}, 409


@product_bp.route('/<int:product_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_product(product_id):
    ''' Update information about a specific product, only allowed for admin'''
    stmt = db.select(Product).filter_by(id=product_id)
    product = db.session.scalar(stmt)

    if product:
        product.name = request.json.get('name') or product.name
        product.description = request.json.get('description') or product.description
        product.price = request.json.get('price') or product.price
        product.stock = request.json.get('stock') or product.stock
        product.category_id = request.json.get('category_id') or product.category_id

        db.session.commit()

        return ProductSchema().dump(product)
    else:
        return {'error': f'Product not found with id {product_id}'}, 404


@product_bp.route('/<int:product_id>/', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    ''' Delete sepecific product, only allowed for admin'''
    # authorize()  # Only allow admin to delete users

    stmt = db.select(Product).filter_by(id=product_id)
    product = db.session.scalar(stmt)

    if product:
        db.session.delete(product)
        db.session.commit()
        return {'message': f"Product with id:{product.id}', name: {product.name}', "
        f" deleted successfully"}
    else:
        return {'error': f'Product not found with id {product_id}'}, 404



@product_bp.route('/category/')
@jwt_required()
def get_all_categories():
    '''Get information about all categoreis, only allowed for admin'''
    stmt = db.select(Category)
    categories = db.session.scalars(stmt)
    return CategorySchema(many=True).dump(categories) 


@product_bp.route('/category/<int:category_id>/')
@jwt_required()
def get_single_category(category_id):
    '''Get information about a specific category'''
    stmt = db.select(Category).filter_by(id=category_id)
    category = db.session.scalar(stmt)
    if category:
        return CategorySchema().dump(category) 
    else:
        return {'error': f'Category not found with id {category_id}'}, 404

@product_bp.route('/category/', methods=['POST'])
@jwt_required()
def create_categories():
    '''Create new categories, only allowed for admin'''
    # authorize()
    try:
        # Create a new Category model instance
        # Request.json returns decode json to dict
        category = Category(
            type = request.json['type']
            )

        db.session.add(category)
        db.session.commit()

        # Response back to the client, user marshmallow to serialize data
        return CategorySchema().dump(category), 201

    except IntegrityError:
        return {'error': 'Category type already exists'}, 409


@product_bp.route('/category/<int:category_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_category(category_id):
    ''' Update information about a specific category, only allowed for admin'''
    stmt = db.select(Category).filter_by(id=category_id)
    category = db.session.scalar(stmt)

    if category:
        category.type = request.json.get('type') or category.type

        db.session.commit()

        return CategorySchema().dump(category)
    else:
        return {'error': f'Category not found with id {category_id}'}, 404


@product_bp.route('/category/<int:category_id>/', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    ''' Delete sepecific category, only allowed for admin'''
    # authorize()  # Only allow admin to delete users

    stmt = db.select(Category).filter_by(id=category_id)
    category = db.session.scalar(stmt)

    if category:
        db.session.delete(category)
        db.session.commit()
        return {'message': f"Category with id:{category.id}'deleted successfully"}
    else:
        return {'error': f'Product not found with id {category_id}'}, 404

@product_bp.route('/review/')
@jwt_required()
def get_all_reviews():
    '''Get information of all reviews'''
    stmt = db.select(Review)
    reviews = db.session.scalars(stmt)
    return ReviewSchema(many=True).dump(reviews) 


@product_bp.route('/review/<int:review_id>/')
@jwt_required()
def get_single_review(review_id):
    '''Get review information about a specific product'''
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)
    if review:
        return ReviewSchema().dump(review) 
    else:
        return {'error': f'Review not found with id {review_id}'}, 404

    
@product_bp.route('/review/customer/<int:review_id>/', methods=['DELETE'])
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