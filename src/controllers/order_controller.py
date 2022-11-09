from flask import Blueprint, request
from init import db, bcrypt
from datetime import date
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.order import Order, OrderSchema
from models.customer import Customer
from models.product import Product
from models.order_detail import OrderDetail, OrderDetailSchema

    
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
    stmt = db.select(OrderDetail)
    order_details = db.session.scalars(stmt)
    return OrderDetailSchema(many=True).dump(order_details) 


@order_bp.route('/detail/<int:order_detail_id>/')
@jwt_required()
def get_single_order_detail(order_detail_id):
    '''Get information about a specific order, only allowed for admin'''
    # authorize()
    stmt = db.select(OrderDetail).filter_by(id=order_detail_id)
    order_detail = db.session.scalar(stmt)
    if order_detail:
        return OrderDetailSchema().dump(order_detail) 
    else:
        return {'error': f'order_detail not found with id {order_detail_id}'}, 404