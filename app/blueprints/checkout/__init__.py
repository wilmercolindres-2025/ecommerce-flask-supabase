"""
Checkout Blueprint - Order checkout process
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.cart import CartService
from app.services.orders import OrderService
from app.services.auth import AuthService, login_required
from app.services.supabase import get_supabase_client
import urllib.parse

checkout_bp = Blueprint('checkout', __name__)


@checkout_bp.route('/')
def index():
    """Checkout step 1: Review cart"""
    cart_items = CartService.get_cart_items()
    
    if not cart_items:
        flash('Tu carrito está vacío', 'warning')
        return redirect(url_for('catalog.index'))
    
    cart_total = CartService.get_cart_total()
    
    return render_template('checkout/index.html',
                         cart_items=cart_items,
                         cart_total=cart_total)


@checkout_bp.route('/datos', methods=['GET', 'POST'])
def customer_info():
    """Checkout step 2: Customer information"""
    cart_items = CartService.get_cart_items()
    
    if not cart_items:
        flash('Tu carrito está vacío', 'warning')
        return redirect(url_for('catalog.index'))
    
    if request.method == 'POST':
        # Save customer info to session
        session['checkout_customer'] = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone')
        }
        
        return redirect(url_for('checkout.shipping'))
    
    # Pre-fill with user data if logged in
    customer_data = session.get('checkout_customer', {})
    
    if AuthService.is_authenticated() and not customer_data:
        user = AuthService.get_current_user()
        if user:
            customer_data = {
                'name': user.get('full_name', ''),
                'email': user.get('email', ''),
                'phone': user.get('phone', '')
            }
    
    return render_template('checkout/customer_info.html',
                         customer_data=customer_data)


@checkout_bp.route('/envio', methods=['GET', 'POST'])
def shipping():
    """Checkout step 3: Shipping information"""
    if not session.get('checkout_customer'):
        return redirect(url_for('checkout.customer_info'))
    
    cart_items = CartService.get_cart_items()
    
    if not cart_items:
        flash('Tu carrito está vacío', 'warning')
        return redirect(url_for('catalog.index'))
    
    if request.method == 'POST':
        shipping_method = request.form.get('shipping_method')
        
        shipping_data = {
            'method': shipping_method,
            'address_line1': request.form.get('address_line1'),
            'address_line2': request.form.get('address_line2'),
            'city': request.form.get('city'),
            'state': request.form.get('state'),
            'municipality': request.form.get('municipality'),
            'postal_code': request.form.get('postal_code'),
            'notes': request.form.get('notes')
        }
        
        # Calculate shipping cost
        if shipping_method == 'pickup':
            shipping_data['cost'] = 0
        else:
            # Get shipping rate for state
            try:
                supabase = get_supabase_client()
                zone = supabase.table('shipping_zones').select('id').eq('name', shipping_data['state']).single().execute()
                
                if zone.data:
                    rate = supabase.table('shipping_rates').select('rate').eq('zone_id', zone.data['id']).single().execute()
                    shipping_data['cost'] = float(rate.data['rate']) if rate.data else 25.00
                else:
                    shipping_data['cost'] = 25.00
            except:
                shipping_data['cost'] = 25.00
        
        session['checkout_shipping'] = shipping_data
        
        return redirect(url_for('checkout.review'))
    
    # Get shipping zones (departments)
    try:
        supabase = get_supabase_client()
        zones = supabase.table('shipping_zones').select('*').eq('type', 'department').order('name').execute()
        departments = zones.data if zones.data else []
    except:
        departments = []
    
    shipping_data = session.get('checkout_shipping', {})
    
    return render_template('checkout/shipping.html',
                         departments=departments,
                         shipping_data=shipping_data)


@checkout_bp.route('/revision')
def review():
    """Checkout step 4: Review order"""
    if not session.get('checkout_customer') or not session.get('checkout_shipping'):
        return redirect(url_for('checkout.index'))
    
    cart_items = CartService.get_cart_items()
    
    if not cart_items:
        flash('Tu carrito está vacío', 'warning')
        return redirect(url_for('catalog.index'))
    
    customer = session.get('checkout_customer')
    shipping = session.get('checkout_shipping')
    
    # Calculate totals
    subtotal = CartService.get_cart_total()
    shipping_cost = shipping.get('cost', 0)
    
    # Apply coupon if exists
    coupon_code = session.get('checkout_coupon')
    discount = 0
    
    if coupon_code:
        coupon_result = OrderService.validate_coupon(coupon_code, subtotal)
        if coupon_result['valid']:
            discount = coupon_result['discount']
    
    tax = 0  # Guatemala IVA if applicable
    total = subtotal + shipping_cost + tax - discount
    
    return render_template('checkout/review.html',
                         cart_items=cart_items,
                         customer=customer,
                         shipping=shipping,
                         subtotal=subtotal,
                         shipping_cost=shipping_cost,
                         tax=tax,
                         discount=discount,
                         total=total,
                         coupon_code=coupon_code)


@checkout_bp.route('/aplicar-cupon', methods=['POST'])
def apply_coupon():
    """Apply coupon code"""
    coupon_code = request.form.get('coupon_code', '').strip().upper()
    
    if not coupon_code:
        flash('Ingresa un código de cupón', 'error')
        return redirect(url_for('checkout.review'))
    
    subtotal = CartService.get_cart_total()
    result = OrderService.validate_coupon(coupon_code, subtotal)
    
    if result['valid']:
        session['checkout_coupon'] = coupon_code
        flash(f'Cupón aplicado: {result["coupon"]["code"]} - Descuento: Q{result["discount"]:.2f}', 'success')
    else:
        flash(f'Cupón inválido: {result["error"]}', 'error')
    
    return redirect(url_for('checkout.review'))


@checkout_bp.route('/confirmar', methods=['POST'])
def confirm():
    """Confirm and create order"""
    if not session.get('checkout_customer') or not session.get('checkout_shipping'):
        return redirect(url_for('checkout.index'))
    
    cart_items = CartService.get_cart_items()
    
    if not cart_items:
        flash('Tu carrito está vacío', 'warning')
        return redirect(url_for('catalog.index'))
    
    customer = session.get('checkout_customer')
    shipping = session.get('checkout_shipping')
    coupon_code = session.get('checkout_coupon')
    
    # Calculate totals
    subtotal = CartService.get_cart_total()
    shipping_cost = shipping.get('cost', 0)
    tax = 0
    discount = 0
    
    if coupon_code:
        coupon_result = OrderService.validate_coupon(coupon_code, subtotal)
        if coupon_result['valid']:
            discount = coupon_result['discount']
    
    # Create order
    order_data = {
        'user_id': session.get('user_id'),
        'customer_email': customer['email'],
        'customer_name': customer['name'],
        'customer_phone': customer['phone'],
        'shipping_address_line1': shipping['address_line1'],
        'shipping_address_line2': shipping.get('address_line2'),
        'shipping_city': shipping['city'],
        'shipping_state': shipping['state'],
        'shipping_municipality': shipping.get('municipality'),
        'shipping_postal_code': shipping.get('postal_code'),
        'shipping_method': shipping['method'],
        'shipping_notes': shipping.get('notes'),
        'shipping_amount': shipping_cost,
        'tax_amount': tax,
        'discount_amount': discount,
        'coupon_code': coupon_code,
        'payment_method': 'sandbox',
        'customer_notes': request.form.get('notes')
    }
    
    result = OrderService.create_order(order_data)
    
    if result['success']:
        order = result['order']
        
        # Clear checkout session
        session.pop('checkout_customer', None)
        session.pop('checkout_shipping', None)
        session.pop('checkout_coupon', None)
        
        flash('¡Pedido creado exitosamente!', 'success')
        return redirect(url_for('checkout.success', order_number=order['order_number']))
    else:
        flash(f'Error al crear pedido: {result["error"]}', 'error')
        return redirect(url_for('checkout.review'))


@checkout_bp.route('/exito/<order_number>')
def success(order_number):
    """Order success page"""
    order = OrderService.get_order_by_number(order_number)
    
    if not order:
        flash('Pedido no encontrado', 'error')
        return redirect(url_for('main.index'))
    
    # Generate WhatsApp message
    whatsapp_message = f"""¡Hola! 👋

Acabo de realizar un pedido en {request.host}

*Pedido:* {order['order_number']}
*Total:* Q{order['total']:.2f}
*Nombre:* {order['customer_name']}

¿Podrían confirmar mi pedido?

¡Gracias!"""
    
    whatsapp_url = f"https://wa.me/{session.get('whatsapp_phone', '+50212345678').replace('+', '')}?text={urllib.parse.quote(whatsapp_message)}"
    
    return render_template('checkout/success.html',
                         order=order,
                         whatsapp_url=whatsapp_url)
