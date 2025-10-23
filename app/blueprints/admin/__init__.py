"""
Admin Blueprint - Administration panel
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.services.auth import admin_required, AuthService
from app.services.products import ProductService
from app.services.orders import OrderService
from app.services.storage import StorageService
from app.services.supabase import get_supabase_admin_client
from datetime import datetime, timedelta
import json

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
@admin_required
def dashboard():
    """Admin dashboard"""
    try:
        supabase = get_supabase_admin_client()
        
        # Get statistics
        # Total products
        products_count = supabase.table('products').select('id', count='exact').execute()
        total_products = products_count.count if hasattr(products_count, 'count') else 0
        
        # Total orders
        orders_count = supabase.table('orders').select('id', count='exact').execute()
        total_orders = orders_count.count if hasattr(orders_count, 'count') else 0
        
        # Total revenue
        orders = supabase.table('orders').select('total').eq('status', 'pagado').execute()
        total_revenue = sum(float(order['total']) for order in orders.data) if orders.data else 0
        
        # Recent orders
        recent_orders = OrderService.get_all_orders(limit=10)
        
        # Low stock products
        low_stock = supabase.table('product_variants').select(
            '*, product:products(name)'
        ).lte('stock', 10).order('stock').limit(10).execute()
        low_stock_products = low_stock.data if low_stock.data else []
        
        # Orders by status
        orders_by_status = {}
        for status in ['nuevo', 'pagado', 'procesando', 'enviado', 'entregado', 'cancelado']:
            count = supabase.table('orders').select('id', count='exact').eq('status', status).execute()
            orders_by_status[status] = count.count if hasattr(count, 'count') else 0
        
        return render_template('admin/dashboard.html',
                             total_products=total_products,
                             total_orders=total_orders,
                             total_revenue=total_revenue,
                             recent_orders=recent_orders,
                             low_stock_products=low_stock_products,
                             orders_by_status=orders_by_status)
    
    except Exception as e:
        flash(f'Error al cargar dashboard: {str(e)}', 'error')
        return render_template('admin/dashboard.html')


# =====================================================
# PRODUCTS MANAGEMENT
# =====================================================

@admin_bp.route('/productos')
@admin_required
def products():
    """Products list"""
    page = int(request.args.get('page', 1))
    per_page = 20
    offset = (page - 1) * per_page
    
    status = request.args.get('status')
    search = request.args.get('search')
    
    products = ProductService.get_products(
        status=status if status else None,
        search=search,
        limit=per_page,
        offset=offset
    )
    
    return render_template('admin/products/index.html',
                         products=products,
                         page=page,
                         per_page=per_page)


@admin_bp.route('/productos/nuevo', methods=['GET', 'POST'])
@admin_required
def create_product():
    """Create new product"""
    if request.method == 'POST':
        user = AuthService.get_current_user()
        
        try:
            # Parse technical specs JSON
            technical_specs = {}
            if request.form.get('technical_specs'):
                try:
                    technical_specs = json.loads(request.form.get('technical_specs'))
                except:
                    pass
            
            product_data = {
                'sku': request.form.get('sku'),
                'name': request.form.get('name'),
                'slug': request.form.get('slug'),
                'short_description': request.form.get('short_description'),
                'description': request.form.get('description'),
                'technical_specs': technical_specs,
                'category_id': request.form.get('category_id'),
                'brand_id': request.form.get('brand_id') if request.form.get('brand_id') else None,
                'base_price': float(request.form.get('base_price')),
                'sale_price': float(request.form.get('sale_price')) if request.form.get('sale_price') else None,
                'tax_rate': float(request.form.get('tax_rate', 0)),
                'cost': float(request.form.get('cost')) if request.form.get('cost') else None,
                'status': request.form.get('status', 'borrador'),
                'is_featured': request.form.get('is_featured') == 'on',
                'meta_title': request.form.get('meta_title'),
                'meta_description': request.form.get('meta_description')
            }
            
            result = ProductService.create_product(product_data, user['id'])
            
            if result['success']:
                flash('Producto creado exitosamente', 'success')
                return redirect(url_for('admin.edit_product', product_id=result['data']['id']))
            else:
                flash(f'Error al crear producto: {result["error"]}', 'error')
        
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    # Get categories and brands
    categories = ProductService.get_categories(is_active=None)
    brands = ProductService.get_brands(is_active=None)
    
    return render_template('admin/products/create.html',
                         categories=categories,
                         brands=brands)


@admin_bp.route('/productos/editar/<product_id>', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    """Edit product"""
    product = ProductService.get_product_by_id(product_id)
    
    if not product:
        flash('Producto no encontrado', 'error')
        return redirect(url_for('admin.products'))
    
    if request.method == 'POST':
        user = AuthService.get_current_user()
        
        try:
            # Parse technical specs JSON
            technical_specs = {}
            if request.form.get('technical_specs'):
                try:
                    technical_specs = json.loads(request.form.get('technical_specs'))
                except:
                    pass
            
            update_data = {
                'sku': request.form.get('sku'),
                'name': request.form.get('name'),
                'slug': request.form.get('slug'),
                'short_description': request.form.get('short_description'),
                'description': request.form.get('description'),
                'technical_specs': technical_specs,
                'category_id': request.form.get('category_id'),
                'brand_id': request.form.get('brand_id') if request.form.get('brand_id') else None,
                'base_price': float(request.form.get('base_price')),
                'sale_price': float(request.form.get('sale_price')) if request.form.get('sale_price') else None,
                'tax_rate': float(request.form.get('tax_rate', 0)),
                'cost': float(request.form.get('cost')) if request.form.get('cost') else None,
                'status': request.form.get('status'),
                'is_featured': request.form.get('is_featured') == 'on',
                'meta_title': request.form.get('meta_title'),
                'meta_description': request.form.get('meta_description')
            }
            
            # Set published_at if status is publicado
            if update_data['status'] == 'publicado' and not product.get('published_at'):
                update_data['published_at'] = datetime.now().isoformat()
            
            result = ProductService.update_product(product_id, update_data, user['id'])
            
            if result['success']:
                flash('Producto actualizado exitosamente', 'success')
                return redirect(url_for('admin.edit_product', product_id=product_id))
            else:
                flash(f'Error al actualizar producto: {result["error"]}', 'error')
        
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    # Get categories and brands
    categories = ProductService.get_categories(is_active=None)
    brands = ProductService.get_brands(is_active=None)
    
    return render_template('admin/products/edit.html',
                         product=product,
                         categories=categories,
                         brands=brands)


@admin_bp.route('/productos/eliminar/<product_id>', methods=['POST'])
@admin_required
def delete_product(product_id):
    """Delete product"""
    result = ProductService.delete_product(product_id)
    
    if result['success']:
        flash('Producto eliminado exitosamente', 'success')
    else:
        flash(f'Error al eliminar producto: {result["error"]}', 'error')
    
    return redirect(url_for('admin.products'))


@admin_bp.route('/productos/<product_id>/imagenes', methods=['POST'])
@admin_required
def upload_product_image(product_id):
    """Upload product image"""
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    # Upload to Supabase Storage
    result = StorageService.upload_product_image(file, product_id)
    
    if result['success']:
        # Save to database
        try:
            supabase = get_supabase_admin_client()
            
            # Check if this is the first image (make it primary)
            existing_images = supabase.table('product_images').select('id').eq('product_id', product_id).execute()
            is_primary = not existing_images.data or len(existing_images.data) == 0
            
            image_data = {
                'product_id': product_id,
                'storage_path': result['path'],
                'url': result['url'],
                'is_primary': is_primary,
                'display_order': len(existing_images.data) if existing_images.data else 0
            }
            
            supabase.table('product_images').insert(image_data).execute()
            
            return jsonify({'success': True, 'url': result['url']})
        
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    else:
        return jsonify({'success': False, 'error': result['error']}), 400


@admin_bp.route('/productos/<product_id>/imagenes/<image_id>/eliminar', methods=['POST'])
@admin_required
def delete_product_image(product_id, image_id):
    """Delete product image"""
    try:
        supabase = get_supabase_admin_client()
        
        # Get image
        image = supabase.table('product_images').select('*').eq('id', image_id).single().execute()
        
        if not image.data:
            return jsonify({'success': False, 'error': 'Image not found'}), 404
        
        # Delete from storage
        StorageService.delete_file('products', image.data['storage_path'])
        
        # Delete from database
        supabase.table('product_images').delete().eq('id', image_id).execute()
        
        return jsonify({'success': True})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# =====================================================
# ORDERS MANAGEMENT
# =====================================================

@admin_bp.route('/pedidos')
@admin_required
def orders():
    """Orders list"""
    page = int(request.args.get('page', 1))
    per_page = 20
    offset = (page - 1) * per_page
    
    status = request.args.get('status')
    
    orders = OrderService.get_all_orders(status=status, limit=per_page, offset=offset)
    
    return render_template('admin/orders/index.html',
                         orders=orders,
                         page=page,
                         per_page=per_page)


@admin_bp.route('/pedidos/<order_id>')
@admin_required
def order_detail(order_id):
    """Order detail"""
    order = OrderService.get_order_by_id(order_id)
    
    if not order:
        flash('Pedido no encontrado', 'error')
        return redirect(url_for('admin.orders'))
    
    return render_template('admin/orders/detail.html', order=order)


@admin_bp.route('/pedidos/<order_id>/actualizar-estado', methods=['POST'])
@admin_required
def update_order_status(order_id):
    """Update order status"""
    status = request.form.get('status')
    admin_notes = request.form.get('admin_notes')
    
    result = OrderService.update_order_status(order_id, status, admin_notes)
    
    if result['success']:
        flash('Estado del pedido actualizado', 'success')
    else:
        flash(f'Error: {result["error"]}', 'error')
    
    return redirect(url_for('admin.order_detail', order_id=order_id))


# =====================================================
# CATEGORIES & BRANDS
# =====================================================

@admin_bp.route('/categorias')
@admin_required
def categories():
    """Categories list"""
    categories = ProductService.get_categories(is_active=None)
    return render_template('admin/categories/index.html', categories=categories)


@admin_bp.route('/marcas')
@admin_required
def brands():
    """Brands list"""
    brands = ProductService.get_brands(is_active=None)
    return render_template('admin/brands/index.html', brands=brands)


# =====================================================
# REPORTS
# =====================================================

@admin_bp.route('/reportes')
@admin_required
def reports():
    """Reports dashboard"""
    return render_template('admin/reports/index.html')


@admin_bp.route('/reportes/ventas')
@admin_required
def sales_report():
    """Sales report"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not start_date:
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    try:
        supabase = get_supabase_admin_client()
        
        # Get orders in date range
        orders = supabase.table('orders').select('*').gte('created_at', start_date).lte('created_at', end_date).eq('status', 'pagado').execute()
        
        total_sales = sum(float(order['total']) for order in orders.data) if orders.data else 0
        total_orders = len(orders.data) if orders.data else 0
        average_order = total_sales / total_orders if total_orders > 0 else 0
        
        return render_template('admin/reports/sales.html',
                             start_date=start_date,
                             end_date=end_date,
                             total_sales=total_sales,
                             total_orders=total_orders,
                             average_order=average_order,
                             orders=orders.data if orders.data else [])
    
    except Exception as e:
        flash(f'Error al generar reporte: {str(e)}', 'error')
        return render_template('admin/reports/sales.html')
