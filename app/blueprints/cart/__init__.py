"""
Cart Blueprint - Shopping cart
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.services.cart import CartService

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/')
def index():
    """Shopping cart page"""
    cart_items = CartService.get_cart_items()
    cart_total = CartService.get_cart_total()
    
    return render_template('cart/index.html',
                         cart_items=cart_items,
                         cart_total=cart_total)


@cart_bp.route('/agregar', methods=['POST'])
def add():
    """Add item to cart"""
    product_id = request.form.get('product_id')
    variant_id = request.form.get('variant_id')
    quantity = int(request.form.get('quantity', 1))
    
    if not product_id:
        if request.headers.get('HX-Request'):
            return jsonify({'success': False, 'error': 'Producto no especificado'}), 400
        flash('Producto no especificado', 'error')
        return redirect(request.referrer or url_for('main.index'))
    
    result = CartService.add_to_cart(product_id, variant_id, quantity)
    
    if result['success']:
        if request.headers.get('HX-Request'):
            # Return updated cart count for HTMX
            cart_count = CartService.get_cart_count()
            return jsonify({'success': True, 'cart_count': cart_count})
        
        flash('Producto agregado al carrito', 'success')
        return redirect(url_for('cart.index'))
    else:
        if request.headers.get('HX-Request'):
            return jsonify({'success': False, 'error': result['error']}), 400
        
        flash(f'Error: {result["error"]}', 'error')
        return redirect(request.referrer or url_for('main.index'))


@cart_bp.route('/actualizar/<item_id>', methods=['POST'])
def update(item_id):
    """Update cart item quantity"""
    quantity = int(request.form.get('quantity', 1))
    
    result = CartService.update_cart_item(item_id, quantity)
    
    if result['success']:
        if request.headers.get('HX-Request'):
            cart_total = CartService.get_cart_total()
            return jsonify({'success': True, 'cart_total': cart_total})
        
        flash('Carrito actualizado', 'success')
    else:
        if request.headers.get('HX-Request'):
            return jsonify({'success': False, 'error': result['error']}), 400
        
        flash(f'Error: {result["error"]}', 'error')
    
    return redirect(url_for('cart.index'))


@cart_bp.route('/eliminar/<item_id>', methods=['POST', 'DELETE'])
def remove(item_id):
    """Remove item from cart"""
    result = CartService.remove_from_cart(item_id)
    
    if result['success']:
        if request.headers.get('HX-Request'):
            cart_count = CartService.get_cart_count()
            cart_total = CartService.get_cart_total()
            return jsonify({'success': True, 'cart_count': cart_count, 'cart_total': cart_total})
        
        flash('Producto eliminado del carrito', 'success')
    else:
        if request.headers.get('HX-Request'):
            return jsonify({'success': False, 'error': result['error']}), 400
        
        flash(f'Error: {result["error"]}', 'error')
    
    return redirect(url_for('cart.index'))


@cart_bp.route('/limpiar', methods=['POST'])
def clear():
    """Clear all items from cart"""
    result = CartService.clear_cart()
    
    if result['success']:
        flash('Carrito vaciado', 'success')
    else:
        flash(f'Error: {result["error"]}', 'error')
    
    return redirect(url_for('cart.index'))


@cart_bp.route('/contador')
def count():
    """Get cart count (for AJAX)"""
    count = CartService.get_cart_count()
    return jsonify({'count': count})
