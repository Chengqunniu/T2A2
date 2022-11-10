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

    
product_bp = Blueprint('product', __name__, url_prefix='/product')  # Create a blueprint for product controller

@product_bp.route('/')
@jwt_required()
def get_all_product():
    '''Get information of all products'''
    stmt = db.select(Product)  # Create SQL statement: select all products
    products = db.session.scalars(stmt)  # Return all products

    # Response back to the client, user marshmallow to serialize data
    return ProductSchema(many=True, exclude=['category_id']).dump(products) 


@product_bp.route('/<int:product_id>/')
@jwt_required()
def get_single_product(product_id):
    '''Get information about a specific product'''
    stmt = db.select(Product).filter_by(id=product_id)  # Create SQL statement : select a product with specific id
    product = db.session.scalar(stmt)  # Return the product found
    # If product exists, return the information of the product
    # If not, return the error message
    if product:

        # Response back to the client, user marshmallow to serialize data
        return ProductSchema(exclude=['category_id']).dump(product) 
    else:
        return {'error': f'Product not found with id {product_id}'}, 404


@product_bp.route('/', methods=['POST'])
@jwt_required()
def create_products():
    '''Allow admin user to create new products'''
    authorize()  # Authorize admin user to perform action, same for the whole project

    data = ProductSchema().load(request.json)  # Use productschema to sanitise and validate data
    # Use try/except to handle IntegrityError, make sure product belongs to an existing category
    try:
        # Create a new product
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
    ''' Allow admin user to update information about a specific product'''
    authorize()

    data = ProductSchema().load(request.json)  # Use productschema to sanitise and validate data

    stmt = db.select(Product).filter_by(id=product_id)  # Create SQL statement : select product with specific id
    product = db.session.scalar(stmt)  # Return the product found
    # If product exists, update it
    # If not, return the error message
    if product:
        # Use try/except to handle IntegrityError, make sure product belongs to an existing category
        try:
            product.name = data['name'] or product.name
            if 'description' in data.keys():
                product.description = data['description'] or product.description
            product.price = data['price'] or product.price
            product.stock = data['stock'] or product.stock
            product.category_id = data['category_id'] or product.category_id

            db.session.commit() 

            # Response back to the client, user marshmallow to serialize data
            return ProductSchema(exclude=['category_id']).dump(product)

        except IntegrityError:
            return {'error': f' Category does not exist.'}
    else:
        return {'error': f'Product not found with id {product_id}'}, 404


@product_bp.route('/<int:product_id>/', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    ''' Allow admin user to delete sepecific product'''
    authorize()
    # Use try/except to handle IntegrityError, if product_id being used as ForeignKey in order_details
    # It can not be deleted
    try:
        stmt = db.select(Product).filter_by(id=product_id)  # Create SQL statement : select product with specific id
        product = db.session.scalar(stmt)  # Return the product found
        # If product exists, delete it
        # If not, return the error message
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
    '''Get information about all categoreis'''
    
    stmt = db.select(Category)  # Create SQL statement : select all categories
    categories = db.session.scalars(stmt)  # Return all categories

    # Response back to the client, user marshmallow to serialize data
    return CategorySchema(many=True).dump(categories) 


@product_bp.route('/category/<int:category_id>/')
@jwt_required()
def get_single_category(category_id):
    '''Get information about a specific category'''

    stmt = db.select(Category).filter_by(id=category_id)  # Create SQL statement : select category with a specific id
    category = db.session.scalar(stmt)  # Return the category found
    # If category exists, return the information of the category
    # If not, return the error message
    if category:
        # Response back to the client, user marshmallow to serialize data
        return CategorySchema().dump(category) 
    else:
        return {'error': f'Category not found with id {category_id}'}, 404


@product_bp.route('/category/', methods=['POST'])
@jwt_required()
def create_categories():
    '''Allow admin user to create new categories'''

    # authorize()

    data = CategorySchema().load(request.json)  # Use CategorySchema to sanitise and validate data
    # Use try/except to handle IntegrityError, make sure category type is unique
    try:
        # Create a new category
        category = Category(
            type = data['type']
            )

        db.session.add(category)
        db.session.commit()

        # Response back to the client, user marshmallow to serialize data
        return CategorySchema().dump(category), 201
    except IntegrityError:
        return {'error': 'Category type has already been used.'}, 409



@product_bp.route('/category/<int:category_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_category(category_id):
    '''Allow admin user to update information about a specific category'''

    authorize()

    stmt = db.select(Category).filter_by(id=category_id)  # Create SQL statement : select category with a specific id
    category = db.session.scalar(stmt)  # Return the category found

    data = CategorySchema().load(request.json)  # Use CategorySchema to sanitise and validate data

    # Use try/except to handle IntegrityError, make sure category type is unique
    try:
        # If category exists, update it
        # If not, return the error message
        if category:
            category.type = data('type') or category.type

            db.session.commit()

            # Response back to the client, user marshmallow to serialize data
            return CategorySchema().dump(category)
        else:
            return {'error': f'Category not found with id {category_id}'}, 404
    except IntegrityError:
        return {'error': 'Category type has already been used.'}, 409


@product_bp.route('/category/<int:category_id>/', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    ''' Allow admin user to delete sepecific category'''
    authorize() 

    stmt = db.select(Category).filter_by(id=category_id)  # Create SQL statement : select category with a specific id
    category = db.session.scalar(stmt)  # Return the category found
    # Use try/except to handle IntegrityError, if category being used as ForeignKey in products
    # It can not be deleted
    try:
        # If category exists, delete it
        # If not, return the error message
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

    # Create SQL statement : select all reviews for a specific product
    stmt = db.select(Review).filter_by(product_id=product_id_entered) 
    reviews = db.session.scalars(stmt)  # Return all reviews for that product
    list_of_reviews = ReviewSchema(many=True).dump(reviews)  # Serialize data
    # If product has no review, return the error message
    # Otherwise, display all reviews
    if list_of_reviews == []:
        return {'error': f'Product with id {product_id_entered} does not have any reviews.'}, 404
    else:
        return list_of_reviews


@product_bp.route('/<int:product_id_entered>/review/<int:review_id>/')
@jwt_required()
def get_single_review(product_id_entered, review_id):
    '''Get a specific review information about a specific product'''

    # Create SQL statement : select a specific review for a specific product
    stmt = db.select(Review).filter_by(id=review_id, product_id=product_id_entered)  
    review = db.session.scalar(stmt)  # Return the review found
    # If review exists, return the review information
    # If not, return the error message
    if review:
        # Response back to the client, user marshmallow to serialize data
        return ReviewSchema().dump(review) 
    else:
        return {'error': f'Review not found with id {review_id}'}, 404


@product_bp.route('/<int:product_id_entered>/review/', methods=['POST'])
@jwt_required()
def create_review(product_id_entered):
    '''Create a review for one product'''
    review_data = ReviewSchema().load(request.json)  # Use reviewschema to sanitise and validate data

    user_id = get_jwt_identity()
    # Create SQL statement : select customer with the user id
    stmt = db.select(Customer).filter_by(user_id=user_id)
    customer = db.session.scalar(stmt)  # Return the customer found
    # Create SQL statement : select product with product_id entered
    stmt = db.select(Product).filter_by(id=product_id_entered)
    product = db.session.scalar(stmt)  # Return the product found
    # If product exists, create review for it
    # If not, return the error message
    if product:
        review = Review(
            comment = review_data['comment'],
            rating = review_data['rating'],
            customer_id = customer.id,
            product_id = product.id
        )
        db.session.add(review)
        db.session.commit()

        # Response back to the client, user marshmallow to serialize data
        return ReviewSchema().dump(review) 
    else:
        return {'error': f'Product with id {product_id_entered} does not exists.'}, 404


@product_bp.route('/<int:product_id_entered>/review/<int:review_id>/', methods=['DELETE'])
@jwt_required()
def delete_review(product_id_entered, review_id):
    '''Delete a review for one product'''

    user_id = get_jwt_identity()
    # Create SQL statement : select customer with the user id
    stmt = db.select(Customer).filter_by(user_id=user_id)
    customer = db.session.scalar(stmt)  # Return the customer found
    # Create SQL statement : select product with product id entered
    stmt = db.select(Product).filter_by(id=product_id_entered)
    product = db.session.scalar(stmt)  # Return the product found
    # If product exists, delete it
    # If not, return the error message
    if product:
        # Create SQL statement : select a review made by logged in customer and with a specific id
        stmt = db.select(Review).filter_by(customer_id=customer.id, id=review_id)
        review = db.session.scalar(stmt)  # Return the review found
        # If review exists, delete it
        # If not, return the error message
        if review:
            db.session.delete(review)
            db.session.commit()
            return {'message': f"Review with id:{review.id} has been deleted successfully."
            f" deleted successfully"}
        else:
            return {'error': f'You do not have the review with id {review_id}'}, 404
    else:
        return {'error': f' Product with id {product_id_entered} does not exists.'}