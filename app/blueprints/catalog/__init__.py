"""
Catalog Blueprint - Products and categories
"""
from flask import Blueprint, render_template, request, abort
from app.services.products import ProductService

catalog_bp = Blueprint('catalog', __name__)


@catalog_bp.route('/')
def index():
    """Catalog home - all products"""
    page = int(request.args.get('page', 1))
    per_page = 20
    offset = (page - 1) * per_page
    
    # Get filters
    category_id = request.args.get('categoria')
    brand_id = request.args.get('marca')
    min_price = request.args.get('precio_min', type=float)
    max_price = request.args.get('precio_max', type=float)
    order_by = request.args.get('orden', 'created_at')
    order_dir = request.args.get('dir', 'desc')
    
    # Get products
    products = ProductService.get_products(
        category_id=category_id,
        brand_id=brand_id,
        min_price=min_price,
        max_price=max_price,
        order_by=order_by,
        order_dir=order_dir,
        limit=per_page,
        offset=offset
    )
    
    # Get categories and brands for filters
    categories = ProductService.get_categories()
    brands = ProductService.get_brands()
    
    return render_template('catalog/index.html',
                         products=products,
                         categories=categories,
                         brands=brands,
                         page=page,
                         per_page=per_page)


@catalog_bp.route('/categoria/<slug>')
def category(slug):
    """Products by category"""
    category = ProductService.get_category_by_slug(slug)
    
    if not category:
        abort(404)
    
    page = int(request.args.get('page', 1))
    per_page = 20
    offset = (page - 1) * per_page
    
    # Get filters
    brand_id = request.args.get('marca')
    min_price = request.args.get('precio_min', type=float)
    max_price = request.args.get('precio_max', type=float)
    order_by = request.args.get('orden', 'created_at')
    order_dir = request.args.get('dir', 'desc')
    
    # Get products
    products = ProductService.get_products(
        category_id=category['id'],
        brand_id=brand_id,
        min_price=min_price,
        max_price=max_price,
        order_by=order_by,
        order_dir=order_dir,
        limit=per_page,
        offset=offset
    )
    
    # Get subcategories
    subcategories = ProductService.get_categories(parent_id=category['id'])
    
    # Get brands for filters
    brands = ProductService.get_brands()
    
    return render_template('catalog/category.html',
                         category=category,
                         subcategories=subcategories,
                         products=products,
                         brands=brands,
                         page=page,
                         per_page=per_page)


@catalog_bp.route('/producto/<slug>')
def product(slug):
    """Product detail page"""
    product = ProductService.get_product_by_slug(slug)
    
    if not product:
        abort(404)
    
    # Get related products
    related_products = ProductService.get_related_products(product['id'])
    
    # If no related products, get products from same category
    if not related_products:
        related_products = ProductService.get_products(
            category_id=product['category_id'],
            limit=4
        )
        # Remove current product
        related_products = [p for p in related_products if p['id'] != product['id']]
    
    return render_template('catalog/product.html',
                         product=product,
                         related_products=related_products)


@catalog_bp.route('/marca/<slug>')
def brand(slug):
    """Products by brand"""
    # Get brand
    try:
        from app.services.supabase import get_supabase_client
        supabase = get_supabase_client()
        brand_response = supabase.table('brands').select('*').eq('slug', slug).single().execute()
        brand = brand_response.data if brand_response.data else None
    except:
        brand = None
    
    if not brand:
        abort(404)
    
    page = int(request.args.get('page', 1))
    per_page = 20
    offset = (page - 1) * per_page
    
    # Get filters
    category_id = request.args.get('categoria')
    min_price = request.args.get('precio_min', type=float)
    max_price = request.args.get('precio_max', type=float)
    order_by = request.args.get('orden', 'created_at')
    order_dir = request.args.get('dir', 'desc')
    
    # Get products
    products = ProductService.get_products(
        brand_id=brand['id'],
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        order_by=order_by,
        order_dir=order_dir,
        limit=per_page,
        offset=offset
    )
    
    # Get categories for filters
    categories = ProductService.get_categories()
    
    return render_template('catalog/brand.html',
                         brand=brand,
                         products=products,
                         categories=categories,
                         page=page,
                         per_page=per_page)
