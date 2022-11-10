from flask import Blueprint, request
from init import db
from datetime import date
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.order import Order, OrderSchema
from models.customer import Customer
from models.product import Product
from models.order_detail import OrderDetail, OrderDetailSchema
from models.order_status import OrderStatus, OrderStatusSchema
from models.shipping_method import ShippingMethod, ShippingMethodSchema
from controllers.user_controller import authorize
from sqlalchemy.exc import IntegrityError


    
order_bp = Blueprint('order', __name__, url_prefix='/order')  # create blueprint for order controller

@order_bp.route('/')
@jwt_required()
def get_all_orders():
    '''Allow admin user to check information for all orders'''

    authorize()  # Authorize admin user to perform action, it's same for the whole project

    stmt = db.select(Order)  # Create SQL statement : select all orders
    orders = db.session.scalars(stmt)  # Return all orders

    # Response back to the client, user marshmallow to serialize data
    return OrderSchema(many=True, exclude=['shipping_method_id']).dump(orders) 


@order_bp.route('/<int:order_id>/')
@jwt_required()
def get_single_order(order_id):
    '''Allow admin user to check information for single order'''

    authorize()

    stmt = db.select(Order).filter_by(id=order_id)  # Create SQL statement : select order by using order_id entered
    order = db.session.scalar(stmt)  # Return the order
    # If order has been found, display the order information
    # If order not found, return the error message
    if order:
        # Response back to the client, user marshmallow to serialize data
        return OrderSchema(exclude=['shipping_method_id']).dump(order) 
    else:
        return {'error': f'order not found with id {order_id}'}, 404


@order_bp.route('/customer/')
@jwt_required()
def get_all_orders_for_specific_customer():
    '''Allow customer to check their own orders'''

    user_id = get_jwt_identity()  # Get the user_id
    stmt = db.select(Customer).filter_by(user_id=user_id)  # Create SQL statement : select customer by using the user_id
    customer = db.session.scalar(stmt)  # Return the customer

    stmt = db.select(Order).filter_by(customer_id=customer.id)  # Create SQL statement : select orders belongs to the customer by using the customer_id
    orders = db.session.scalars(stmt)  # Return orders for the customer
    # Response back to the client, user marshmallow to serialize data
    return OrderSchema(many=True, exclude=['shipping_method_id']).dump(orders) 


@order_bp.route('/customer/', methods=['POST'])
@jwt_required()
def create_order():
    '''Create order for the customer'''

    user_id = get_jwt_identity()  # Get the user_id
    stmt = db.select(Customer).filter_by(user_id=user_id)  # Create SQL statement : select customer by using the user_id
    customer = db.session.scalar(stmt)  # Return the customer

    order_data = OrderSchema().load(request.json)  # Use orderschema to sanitise and validate data

    # Create a new order
    order = Order(
        order_date = date.today(),
        customer_id = customer.id,
        shipping_method_id = order_data['shipping_method_id']
        )

    db.session.add(order)
    db.session.commit()

    # Response back to the client, user marshmallow to serialize data
    return OrderSchema(exclude=['shipping_method_id', 'order_status_id']).dump(order) 

@order_bp.route('/detail/', methods=['POST'])
def create_order_detail():
    ''' Create a new order detail'''

    detail_data = OrderDetailSchema().load(request.json)  # User orderdetailschema to sanitise and validate data

    try:  # User try/except to handle IntegrityError, order_id and product_id must exist
    # Create a new orderdetail
        order_detail = OrderDetail(
            price = detail_data['price'],
            quantity = detail_data['quantity'],
            order_id = detail_data['order_id'],
            product_id = detail_data['product_id']
            )
            
        db.session.add(order_detail)
        db.session.commit()

        # Response back to the client, user marshmallow to serialize data
        return OrderDetailSchema(exclude=['order_id', "product_id"]).dump(order_detail)

    except IntegrityError:
        return {'error': 'Please check order_id and product_id'}


@order_bp.route('/detail/')
@jwt_required()
def get_all_details():
    '''Allow admin user to get all order details'''

    authorize()  # Only allow admin user to check information of all details
    stmt = db.select(OrderDetail)  # Create SQL statement : select all order_details
    order_details = db.session.scalars(stmt)  # Return all order_details

    # Response back to the client, user marshmallow to serialize data
    return OrderDetailSchema(many=True).dump(order_details) 


@order_bp.route('/detail/<int:order_detail_id>/')
@jwt_required()
def get_single_order_detail(order_detail_id):
    '''Allow admin user to get single order detail'''

    authorize()
    stmt = db.select(OrderDetail).filter_by(id=order_detail_id)  # Create SQL statement : select order_detail by using order_detail id entered
    order_detail = db.session.scalar(stmt)  # Return the order_detail
    # If order_detail exists, return the information of it
    # If not exists, return error message
    if order_detail:
        # Response back to the client, user marshmallow to serialize data
        return OrderDetailSchema().dump(order_detail) 
    else:
        return {'error': f'order_detail not found with id {order_detail_id}'}, 404


@order_bp.route('/status/')
@jwt_required()
def get_all_order_statues():
    '''Allow admin user to get all order statues'''

    authorize() 
    stmt = db.select(OrderStatus)  # Create SQL statement : select all order statuses
    order_statues = db.session.scalars(stmt)  #  Return order_statues

    # Response back to the client, user marshmallow to serialize data
    return OrderStatusSchema(many=True).dump(order_statues) 


@order_bp.route('/status/<int:order_status_id>/')
@jwt_required()
def get_single_order_status(order_status_id):
    '''Allow admin user to get a single order status'''

    authorize() 
    stmt = db.select(OrderStatus).filter_by(id=order_status_id)  # Create SQL statement : select order status using the order_status id entered
    order_status = db.session.scalar(stmt)  # Return the order_status
    # If order_status exists, return the information of the order_status
    # If not exists, return error message
    if order_status:
        # Response back to the client, user marshmallow to serialize data
        return OrderStatusSchema().dump(order_status) 
    else:
        return {'error': f'order_status not found with id {order_status_id}'}, 404


@order_bp.route('/status/', methods=['POST'])
@jwt_required()
def create_order_statues():
    '''Get information about all order statues, only allowed for admin'''

    authorize()

    data = OrderStatusSchema().load(request.json)  # User orderstatusschema to sanitise and validate data

    # Use try/except to handle IntegrityError, type is unique
    try:
        # Create a new order status
        order_statues = OrderStatus(
            type=data['type']
            )

        db.session.add(order_statues)
        db.session.commit()

        # Response back to the client, user marshmallow to serialize data
        return OrderStatusSchema().dump(order_statues), 201

    except IntegrityError:
        return {'error': 'Order Status type already in use'}, 409


@order_bp.route('/status/<int:order_status_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_order_status(order_status_id):
    ''' Update order status'''

    authorize()

    data = OrderStatusSchema().load(request.json)  # Use orderstatusschema to sanitise and validate data

    stmt = db.select(OrderStatus).filter_by(id=order_status_id)  # Create SQL statement : select order_status using order_status id
    order_status = db.session.scalar(stmt)  # Return the order_status found

    # If order_status exists, update order status
    # If not, return the error message
    if order_status:
        order_status.type = data['type'] or order_status.type

        db.session.commit()

        return OrderStatusSchema().dump(order_status)
    else:
        return {'error': f'order_status not found with id {order_status_id}'}, 404


@order_bp.route('/status/<int:order_status_id>/', methods=['DELETE'])
@jwt_required()
def delete_order_status(order_status_id):
    ''' Delete order status'''

    authorize()

    stmt = db.select(OrderStatus).filter_by(id=order_status_id)  # Create SQL statement : select order_status using the order_status id
    order_status = db.session.scalar(stmt)  # Return the order_status found
    # Use try/except to handle IntegrityError, if the order_status has related orders, it can not be deleted
    try:
        # If order_status exists with the id, delete it
        # If not, return error message
        if order_status:
            db.session.delete(order_status)
            db.session.commit()
            return {'message': f"Order status with id:{order_status.id}', type:'{order_status.type}' deleted successfully"}
        else:
            return {'error': f'Order status not found with id {order_status_id}'}, 404
    except IntegrityError:
        return {'error': 'You can not delete this order status.'}, 409


@order_bp.route('/shipping/')
@jwt_required()
def get_all_shipping_methods():
    '''Allow admin user to get information of all shipping methods'''

    authorize()
    stmt = db.select(ShippingMethod)  # Create SQL statement : select all shipping methods
    shipping_methods = db.session.scalars(stmt)  # Return all shipping methods

    # Response back to the client, user marshmallow to serialize data
    return ShippingMethodSchema(many=True).dump(shipping_methods) 


@order_bp.route('/shipping/<int:shipping_method_id>/')
@jwt_required()
def get_single_shipping_method(shipping_method_id):
    '''Allow admin user to get information about a specific shipping method'''
    authorize()
    stmt = db.select(ShippingMethod).filter_by(id=shipping_method_id)  # Create SQL statement : select shipping method with specific id
    shipping_method = db.session.scalar(stmt)  # Return the shipping method found
    # If shipping method exists, return the information
    # If not, return the error message
    if shipping_method:
        
        # Response back to the client, user marshmallow to serialize data
        return ShippingMethodSchema().dump(shipping_method) 
    else:
        return {'error': f'Shipping method not found with id {shipping_method_id}'}, 404


@order_bp.route('/shipping/', methods=['POST'])
@jwt_required()
def create_shiping_methods():
    '''Allow admin user to create new shipping method'''

    authorize()

    data = ShippingMethodSchema().load(request.json)  # Use shippingmethodschema to sanitise and validate data

    # Use try/except to handle IntegrityError, the type of shipping method is unique
    try:
        # Create a new shipping method
        shipping_method = ShippingMethod(
            type = data['type'],
            price = data['price']
            )

        db.session.add(shipping_method)
        db.session.commit()

        # Response back to the client, user marshmallow to serialize data
        return ShippingMethodSchema().dump(shipping_method), 201

    except IntegrityError:
        return {'error': 'Shipping Method type already in use'}, 409


@order_bp.route('/shipping/<int:shipping_method_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_shipping_method(shipping_method_id):
    ''' Update information about a specific shipping method'''
    authorize()
    
    data = ShippingMethodSchema().load(request.json)  # Use shippingmethodschema to sanitise and validate data

    stmt = db.select(ShippingMethod).filter_by(id=shipping_method_id)  # Create SQL statement : select shipping method with sepecific method id
    shipping_method = db.session.scalar(stmt)  # Return the shipping_method found

    # If shipping method exists, update it
    # If not, return the error message
    if shipping_method:
        if 'type' in data.keys():
            shipping_method.type = data['type'] or shipping_method.type
        shipping_method.price = data['price'] or shipping_method.price

        db.session.commit()

        # Response back to the client, user marshmallow to serialize data
        return OrderStatusSchema().dump(shipping_method)
    else:
        return {'error': f'Shipping method not found with id {shipping_method_id}'}, 404


@order_bp.route('/shipping/<int:shipping_method_id>/', methods=['DELETE'])
@jwt_required()
def delete_one_shipping_method(shipping_method_id):
    ''' Allow admin user to delete a shipping method'''
    authorize()
  
    stmt = db.select(ShippingMethod).filter_by(id=shipping_method_id)  # Create SQL statement : select shipping method with specific id
    shipping_method = db.session.scalar(stmt)  # Return the shipping_method found
    # Use try/except to handle IntegrityError, if shipping_method being used as ForeignKey in orders table
    # It can not be deleted
    try:
        # If shipping method exists with the id, delete it
        # If not, return error message
        if shipping_method:
            db.session.delete(shipping_method)
            db.session.commit()
            return {'message': f"Shipping method with id:{shipping_method.id}', type:'{shipping_method.type}', "
            f"price: {shipping_method.price} deleted successfully"}
        else:
            return {'error': f'Shipping method not found with id {shipping_method_id}'}, 404
    except IntegrityError:
        return {'error': 'You can not delete this shipping method.'}, 409