from flask import Blueprint, request
from init import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.product import Product, ProductSchema
from models.category import Category, CategorySchema
from models.review import Review, ReviewSchema
from models.customer import Customer
from sqlalchemy.exc import IntegrityError
from controllers.user_controller import authorize
from datetime import date

    
product_bp = Blueprint('product', __name__, url_prefix='/product')

@product_bp.route('/')
@jwt_required()
def get_all_product():
    '''Get information about all products'''
    stmt = db.select(Product)
    products = db.session.scalars(stmt)
    return ProductSchema(many=True, exclude=['category_id']).dump(products) 


@product_bp.route('/<int:product_id>/')
@jwt_required()
def get_single_product(product_id):
    '''Get information about a specific product'''
    stmt = db.select(Product).filter_by(id=product_id)
    product = db.session.scalar(stmt)
    if product:
        return ProductSchema(exclude=['category_id']).dump(product) 
    else:
        return {'error': f'Product not found with id {product_id}'}, 404


@product_bp.route('/', methods=['POST'])
@jwt_required()
def create_products():
    '''Create new products, only allowed for admin'''
    # authorize()

    data = ProductSchema().load(request.json)

    try:
        # Create a new Product Method model instance
        # Request.json returns decode json to dict
        product = Product(
            name = data['name'],
            description = data['description'],
            price = data['price'],
            stock = data['stock'],
            category_id = data['category_id'],
            create_date = date.today()
            )

        db.session.add(product)
        db.session.commit()

        # Response back to the client, user marshmallow to serialize data
        return ProductSchema(exclude=['category_id']).dump(product), 201

    except IntegrityError:
        return {'error': 'Category does not exists.'}, 409


@product_bp.route('/<int:product_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_product(product_id):
    ''' Update information about a specific product, only allowed for admin'''
    authorize()

    data = ProductSchema().load(request.json)

    stmt = db.select(Product).filter_by(id=product_id)
    product = db.session.scalar(stmt)
    if product:
        try:
            product.name = data['name'] or product.name
            if 'description' in data.keys():
                product.description = data['description'] or product.description
            product.price = data['price'] or product.price
            product.stock = data['stock'] or product.stock
            product.category_id = data['category_id'] or product.category_id

            db.session.commit() 

            return ProductSchema(exclude=['category_id']).dump(product)

        except IntegrityError:
            return {'error': f' Category does not exist.'}
    else:
        return {'error': f'Product not found with id {product_id}'}, 404


@product_bp.route('/<int:product_id>/', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    ''' Delete sepecific product, only allowed for admin'''
    authorize()  # Only allow admin to delete 
    try:
        stmt = db.select(Product).filter_by(id=product_id)
        product = db.session.scalar(stmt)

        if product:
            db.session.delete(product)
            db.session.commit()
            return {'message': f"Product with id:{product.id}', name: {product.name}', "
            f" deleted successfully"}
        else:
            return {'error': f'Product not found with id {product_id}'}, 404
    except IntegrityError:
        return {'error': 'You can not delete this product.'}, 409



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

    data = CategorySchema().load(request.json)

    try:
        # Create a new Category model instance
        # Request.json returns decode json to dict
        category = Category(
            type = data['type']
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

    data = CategorySchema().load(request.json)

    if category:
        category.type = data('type') or category.type

        db.session.commit()

        return CategorySchema().dump(category)
    else:
        return {'error': f'Category not found with id {category_id}'}, 404


@product_bp.route('/category/<int:category_id>/', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    ''' Delete sepecific category, only allowed for admin'''
    authorize()  # Only allow admin to delete category

    stmt = db.select(Category).filter_by(id=category_id)
    category = db.session.scalar(stmt)
    try:
        if category:
            db.session.delete(category)
            db.session.commit()
            return {'message': f"Category with id:{category.id}'deleted successfully"}
        else:
            return {'error': f'Category not found with id {category_id}'}, 404
    except IntegrityError:
        return {'error': 'You can not delete this category.'}, 409


@product_bp.route('/<int:product_id_entered>/review/')
@jwt_required()
def get_all_reviews(product_id_entered):
    '''Get information of all reviews for one product'''
    
    stmt = db.select(Review).filter_by(product_id=product_id_entered)
    reviews = db.session.scalars(stmt)
    list_of_reviews = ReviewSchema(many=True).dump(reviews)
    if list_of_reviews == []:
        return {'error': f'Product with id {product_id_entered} does not have any reviews.'}, 404
    else:
        return list_of_reviews


@product_bp.route('/<int:product_id_entered>/review/<int:review_id>/')
@jwt_required()
def get_single_review(product_id_entered, review_id):
    '''Get a specific review information about a specific product'''
    stmt = db.select(Review).filter_by(id=review_id, product_id=product_id_entered)
    review = db.session.scalar(stmt)
    if review:
        return ReviewSchema().dump(review) 
    else:
        return {'error': f'Review not found with id {review_id}'}, 404


@product_bp.route('/<int:product_id_entered>/review/', methods=['POST'])
@jwt_required()
def create_review(product_id_entered):
    '''Create a review for one product'''
    review_data = ReviewSchema().load(request.json)  # Use reviewschema to sanitise and validate data

    user_id = get_jwt_identity()
    
    stmt = db.select(Customer).filter_by(user_id=user_id)
    customer = db.session.scalar(stmt)

    stmt = db.select(Product).filter_by(id=product_id_entered)
    product = db.session.scalar(stmt)
    if product:
        review = Review(
            comment = review_data['comment'],
            rating = review_data['rating'],
            customer_id = customer.id,
            product_id = product.id
        )
        db.session.add(review)
        db.session.commit()
        return ReviewSchema().dump(review) 
    else:
        return {'error': f'Product with id {product_id_entered} does not exists.'}, 404


@product_bp.route('/<int:product_id_entered>/review/<int:review_id>/', methods=['DELETE'])
@jwt_required()
def delete_review(product_id_entered, review_id):
    '''Create a review for one product'''

    user_id = get_jwt_identity()
    
    stmt = db.select(Customer).filter_by(user_id=user_id)
    customer = db.session.scalar(stmt)

    stmt = db.select(Product).filter_by(id=product_id_entered)
    product = db.session.scalar(stmt)
    if product:

        stmt = db.select(Review).filter_by(customer_id=customer.id, id=review_id)
        review = db.session.scalar(stmt)

        if review:
            db.session.delete(review)
            db.session.commit()
            return {'message': f"Review with id:{review.id} has been deleted successfully."
            f" deleted successfully"}
        else:
            return {'error': f'You do not have the review with id {review_id}'}, 404
    else:
        return {'error': f' Product with id {product_id_entered} does not exists.'}