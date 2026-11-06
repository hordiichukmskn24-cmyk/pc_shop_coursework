from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from database import db
from models.cart import CartItem
from models.order import Order, OrderItem
from services.strategies import CourierDelivery, PostalDelivery, PickupDelivery, OrderCheckoutContext
from services.observers import OrderStatusSubject, EmailNotificationObserver, AdminAuditObserver

order_bp = Blueprint('order', __name__, url_prefix='/order')

@order_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Ваша корзина пуста!', 'warning')
        return redirect(url_for('main.catalog'))
        
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    
    # Стратегии доставки (GoF Strategy Pattern)
    strategies = {
        'courier': CourierDelivery(),
        'postal': PostalDelivery(),
        'pickup': PickupDelivery()
    }
    
    if request.method == 'POST':
        shipping_type = request.form.get('shipping_method', 'postal')
        selected_strategy = strategies.get(shipping_type, PostalDelivery())
        
        context = OrderCheckoutContext(selected_strategy)
        final_price = context.calculate_final_price(subtotal)
        
        # Создание заказа
        order = Order(
            user_id=current_user.id,
            total_price=final_price,
            shipping_method=selected_strategy.get_name(),
            status='New'
        )
        db.session.add(order)
        db.session.flush()
        
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_purchase=item.product.price
            )
            db.session.add(order_item)
            # Очистка корзины
            db.session.delete(item)
            
        db.session.commit()
        
        # Уведомления (GoF Observer Pattern)
        subject = OrderStatusSubject()
        subject.attach(EmailNotificationObserver())
        subject.attach(AdminAuditObserver())
        subject.notify(order.id, 'New')
        
        flash(f'Заказ #{order.id} успешно оформлен!', 'success')
        return redirect(url_for('order.my_orders'))
        
    return render_template('checkout.html', cart_items=cart_items, subtotal=subtotal)

@order_bp.route('/my-orders')
@login_required
def my_orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('my_orders.html', orders=orders)