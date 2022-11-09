from flask import Blueprint, request
from init import db, bcrypt
from datetime import date
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.order import Order, OrderSchema
from models.customer import Customer
from models.product import Product
from models.order_detail import OrderDetail, OrderDetailSchema
from models.order_status import OrderStatus, OrderStatusSchema
from models.shipping_method import ShippingMethod, ShippingMethodSchema
from sqlalchemy.exc import IntegrityError


    
order_bp = Blueprint('order', __name__, url_prefix='/order')

@order_bp.route('/')
@jwt_required()
def get_all_orders():
    '''Get information about all orders, only allowed for admin'''
    # authorize()
    stmt = db.select(Order)
    orders = db.session.scalars(stmt)
    return OrderSchema(many=True, exclude=['shipping_method_id']).dump(orders) 


@order_bp.route('/<int:order_id>/')
@jwt_required()
def get_single_order(order_id):
    '''Get information about a specific order, only allowed for admin'''
    # authorize()
    stmt = db.select(Order).filter_by(id=order_id)
    order = db.session.scalar(stmt)
    if order:
        return OrderSchema(exclude=['shipping_method_id']).dump(order) 
    else:
        return {'error': f'order not found with id {order_id}'}, 404



@order_bp.route('/customer/')
@jwt_required()
def get_all_orders_for_specific_customer():
    '''Get information about all orders for the logged in customer only'''
    user_id = get_jwt_identity()
    stmt = db.select(Customer).filter_by(user_id=user_id)
    customer = db.session.scalar(stmt)

    stmt = db.select(Order).filter_by(customer_id=customer.id)
    orders = db.session.scalars(stmt)
    return OrderSchema(many=True, exclude=['shipping_method_id']).dump(orders) 

@order_bp.route('/customer/', methods=['POST'])
@jwt_required()
def create_order():
    '''Get information about all orders for the logged in customer only'''
    user_id = get_jwt_identity()
    stmt = db.select(Customer).filter_by(user_id=user_id)
    customer = db.session.scalar(stmt)

    order_date = OrderSchema().load(request.json)

    order = Order(
        order_date = date.today(),
        customer_id = customer.id,
        shipping_method_id = order_date['shipping_method_id']
        )

    db.session.add(order)
    db.session.commit()

    for each_order in order_date['order_details']:
        product_entered = each_order['product']
        stmt = db.select(Product).filter_by(name=product_entered['name'])
        product = db.session.scalar(stmt)

        order_detail = OrderDetail(
            price = each_order['price'],
            quantity = each_order['quantity'],
            order_id = order.id,
            product_id = product.id
            )
            
        db.session.add(order_detail)
        db.session.commit()

    return OrderSchema(exclude=['shipping_method_id']).dump(order) 

@order_bp.route('/detail/')
@jwt_required()
def get_all_details():
    '''Get information about all order details, only allowed for admin'''
    # authorize()
    stmt = db.select(OrderDetail)
    order_details = db.session.scalars(stmt)
    return OrderDetailSchema(many=True).dump(order_details) 


@order_bp.route('/detail/<int:order_detail_id>/')
@jwt_required()
def get_single_order_detail(order_detail_id):
    '''Get information about a specific order detail, only allowed for admin'''
    # authorize()
    stmt = db.select(OrderDetail).filter_by(id=order_detail_id)
    order_detail = db.session.scalar(stmt)
    if order_detail:
        return OrderDetailSchema().dump(order_detail) 
    else:
        return {'error': f'order_detail not found with id {order_detail_id}'}, 404


@order_bp.route('/status/')
@jwt_required()
def get_all_order_statues():
    '''Get information about all order statues, only allowed for admin'''
    # authorize()
    stmt = db.select(OrderStatus)
    order_statues = db.session.scalars(stmt)
    return OrderStatusSchema(many=True).dump(order_statues) 


@order_bp.route('/status/<int:order_status_id>/')
@jwt_required()
def get_single_order_status(order_status_id):
    '''Get information about a specific order, only allowed for admin'''
    # authorize()
    stmt = db.select(OrderStatus).filter_by(id=order_status_id)
    order_status = db.session.scalar(stmt)
    if order_status:
        return OrderStatusSchema().dump(order_status) 
    else:
        return {'error': f'order_status not found with id {order_status_id}'}, 404


@order_bp.route('/status/', methods=['POST'])
@jwt_required()
def create_order_statues():
    '''Get information about all order statues, only allowed for admin'''
    # authorize()
    try:
        # Create a new User model instance
        # Request.json returns decode json to dict
        order_statues = OrderStatus(
            type=request.json['type']
            )

        db.session.add(order_statues)
        db.session.commit()

        # Response back to the client, user marshmallow to serialize data
        return OrderStatusSchema().dump(order_statues), 201

    except IntegrityError:
        return {'error': 'Order Status type already in use'}, 409


@order_bp.route('/status/<int:order_status_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_user(order_status_id):
    ''' Update information about a specific user'''
    stmt = db.select(OrderStatus).filter_by(id=order_status_id)
    order_status = db.session.scalar(stmt)

    if order_status:
        order_status.type = request.json.get('type') or order_status.type

        db.session.commit()

        return OrderStatusSchema().dump(order_status)
    else:
        return {'error': f'order_status not found with id {order_status_id}'}, 404


@order_bp.route('/status/<int:order_status_id>/', methods=['DELETE'])
@jwt_required()
def delete_one_user(order_status_id):
    ''' Delete sepecific user'''
    # authorize()  # Only allow admin to delete users

    stmt = db.select(OrderStatus).filter_by(id=order_status_id)
    order_status = db.session.scalar(stmt)

    if order_status:
        db.session.delete(order_status)
        db.session.commit()
        return {'message': f"Order status with id:{order_status.id}', type:'{order_status.type}' deleted successfully"}
    else:
        return {'error': f'Order status not found with id {order_status_id}'}, 404


@order_bp.route('/shipping/')
@jwt_required()
def get_all_shipping_methods():
    '''Get information about all shipping methods, only allowed for admin'''
    # authorize()
    stmt = db.select(ShippingMethod)
    shipping_methods = db.session.scalars(stmt)
    return ShippingMethodSchema(many=True).dump(shipping_methods) 


@order_bp.route('/shipping/<int:shipping_method_id>/')
@jwt_required()
def get_single_shipping_method(shipping_method_id):
    '''Get information about a specific shipping method, only allowed for admin'''
    # authorize()
    stmt = db.select(ShippingMethod).filter_by(id=shipping_method_id)
    shipping_method = db.session.scalar(stmt)
    if shipping_method:
        return ShippingMethodSchema().dump(shipping_method) 
    else:
        return {'error': f'Shipping method not found with id {shipping_method_id}'}, 404


@order_bp.route('/shipping/', methods=['POST'])
@jwt_required()
def create_shiping_methods():
    '''Create new shipping methods, only allowed for admin'''
    # authorize()
    try:
        # Create a new Shipping Method model instance
        # Request.json returns decode json to dict
        shipping_method = ShippingMethod(
            type = request.json['type'],
            price = request.json['price']
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
    ''' Update information about a specific user'''
    stmt = db.select(ShippingMethod).filter_by(id=shipping_method_id)
    shipping_method = db.session.scalar(stmt)

    if shipping_method:
        shipping_method.type = request.json.get('type') or shipping_method.type
        shipping_method.price = request.json.get('price') or shipping_method.price

        db.session.commit()

        return OrderStatusSchema().dump(shipping_method)
    else:
        return {'error': f'Shipping method not found with id {shipping_method_id}'}, 404


@order_bp.route('/shipping/<int:shipping_method_id>/', methods=['DELETE'])
@jwt_required()
def delete_one_shipping_method(shipping_method_id):
    ''' Delete sepecific shipping method'''
    # authorize()  # Only allow admin to delete users

    stmt = db.select(ShippingMethod).filter_by(id=shipping_method_id)
    shipping_method = db.session.scalar(stmt)

    if shipping_method:
        db.session.delete(shipping_method)
        db.session.commit()
        return {'message': f"Shipping method with id:{shipping_method.id}', type:'{shipping_method.type}', "
        f"price: {shipping_method.price} deleted successfully"}
    else:
        return {'error': f'Shipping method not found with id {shipping_method_id}'}, 404