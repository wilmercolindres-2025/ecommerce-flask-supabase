"""
User Blueprint - User account management
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.auth import AuthService, login_required
from app.services.orders import OrderService
from app.services.supabase import get_supabase_admin_client

user_bp = Blueprint('user', __name__)


@user_bp.route('/')
@login_required
def dashboard():
    """User dashboard"""
    user = AuthService.get_current_user()
    
    # Get recent orders
    orders = OrderService.get_user_orders(user['id'], limit=5)
    
    return render_template('user/dashboard.html',
                         user=user,
                         orders=orders)


@user_bp.route('/perfil', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile"""
    user = AuthService.get_current_user()
    
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        
        try:
            supabase = get_supabase_admin_client()
            supabase.table('app_users').update({
                'full_name': full_name,
                'phone': phone
            }).eq('id', user['id']).execute()
            
            flash('Perfil actualizado exitosamente', 'success')
            return redirect(url_for('user.profile'))
        
        except Exception as e:
            flash(f'Error al actualizar perfil: {str(e)}', 'error')
    
    return render_template('user/profile.html', user=user)


@user_bp.route('/pedidos')
@login_required
def orders():
    """User orders"""
    user = AuthService.get_current_user()
    page = int(request.args.get('page', 1))
    per_page = 10
    offset = (page - 1) * per_page
    
    orders = OrderService.get_user_orders(user['id'], limit=per_page, offset=offset)
    
    return render_template('user/orders.html',
                         orders=orders,
                         page=page,
                         per_page=per_page)


@user_bp.route('/pedido/<order_id>')
@login_required
def order_detail(order_id):
    """Order detail"""
    user = AuthService.get_current_user()
    order = OrderService.get_order_by_id(order_id)
    
    if not order or order['user_id'] != user['id']:
        flash('Pedido no encontrado', 'error')
        return redirect(url_for('user.orders'))
    
    return render_template('user/order_detail.html', order=order)


@user_bp.route('/direcciones')
@login_required
def addresses():
    """User addresses"""
    user = AuthService.get_current_user()
    
    try:
        supabase = get_supabase_admin_client()
        addresses = supabase.table('addresses').select('*').eq('user_id', user['id']).execute()
        addresses = addresses.data if addresses.data else []
    except:
        addresses = []
    
    return render_template('user/addresses.html', addresses=addresses)


@user_bp.route('/direcciones/nueva', methods=['GET', 'POST'])
@login_required
def add_address():
    """Add new address"""
    user = AuthService.get_current_user()
    
    if request.method == 'POST':
        try:
            supabase = get_supabase_admin_client()
            
            address_data = {
                'user_id': user['id'],
                'label': request.form.get('label'),
                'full_name': request.form.get('full_name'),
                'phone': request.form.get('phone'),
                'address_line1': request.form.get('address_line1'),
                'address_line2': request.form.get('address_line2'),
                'city': request.form.get('city'),
                'state_department': request.form.get('state_department'),
                'municipality': request.form.get('municipality'),
                'postal_code': request.form.get('postal_code'),
                'is_default': request.form.get('is_default') == 'on'
            }
            
            # If this is default, unset other defaults
            if address_data['is_default']:
                supabase.table('addresses').update({'is_default': False}).eq('user_id', user['id']).execute()
            
            supabase.table('addresses').insert(address_data).execute()
            
            flash('Dirección agregada exitosamente', 'success')
            return redirect(url_for('user.addresses'))
        
        except Exception as e:
            flash(f'Error al agregar dirección: {str(e)}', 'error')
    
    return render_template('user/add_address.html')


@user_bp.route('/direcciones/editar/<address_id>', methods=['GET', 'POST'])
@login_required
def edit_address(address_id):
    """Edit address"""
    user = AuthService.get_current_user()
    
    try:
        supabase = get_supabase_admin_client()
        address = supabase.table('addresses').select('*').eq('id', address_id).eq('user_id', user['id']).single().execute()
        address = address.data if address.data else None
    except:
        address = None
    
    if not address:
        flash('Dirección no encontrada', 'error')
        return redirect(url_for('user.addresses'))
    
    if request.method == 'POST':
        try:
            update_data = {
                'label': request.form.get('label'),
                'full_name': request.form.get('full_name'),
                'phone': request.form.get('phone'),
                'address_line1': request.form.get('address_line1'),
                'address_line2': request.form.get('address_line2'),
                'city': request.form.get('city'),
                'state_department': request.form.get('state_department'),
                'municipality': request.form.get('municipality'),
                'postal_code': request.form.get('postal_code'),
                'is_default': request.form.get('is_default') == 'on'
            }
            
            # If this is default, unset other defaults
            if update_data['is_default']:
                supabase.table('addresses').update({'is_default': False}).eq('user_id', user['id']).execute()
            
            supabase.table('addresses').update(update_data).eq('id', address_id).execute()
            
            flash('Dirección actualizada exitosamente', 'success')
            return redirect(url_for('user.addresses'))
        
        except Exception as e:
            flash(f'Error al actualizar dirección: {str(e)}', 'error')
    
    return render_template('user/edit_address.html', address=address)


@user_bp.route('/direcciones/eliminar/<address_id>', methods=['POST'])
@login_required
def delete_address(address_id):
    """Delete address"""
    user = AuthService.get_current_user()
    
    try:
        supabase = get_supabase_admin_client()
        supabase.table('addresses').delete().eq('id', address_id).eq('user_id', user['id']).execute()
        
        flash('Dirección eliminada exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar dirección: {str(e)}', 'error')
    
    return redirect(url_for('user.addresses'))


@user_bp.route('/cambiar-contrasena', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change password"""
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not new_password or not confirm_password:
            flash('Todos los campos son requeridos', 'error')
            return render_template('user/change_password.html')
        
        if new_password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('user/change_password.html')
        
        if len(new_password) < 8:
            flash('La contraseña debe tener al menos 8 caracteres', 'error')
            return render_template('user/change_password.html')
        
        result = AuthService.update_password(new_password)
        
        if result['success']:
            flash('Contraseña actualizada exitosamente', 'success')
            return redirect(url_for('user.dashboard'))
        else:
            flash('Error al actualizar contraseña', 'error')
    
    return render_template('user/change_password.html')
