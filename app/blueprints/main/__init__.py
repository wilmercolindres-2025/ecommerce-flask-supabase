"""
Main Blueprint - Home and static pages
"""
from flask import Blueprint, render_template, request
from app.services.products import ProductService
from app.services.supabase import get_supabase_client

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Home page"""
    # Get featured products
    featured_products = ProductService.get_featured_products(limit=8)
    
    # Get active banners
    try:
        supabase = get_supabase_client()
        banners = supabase.table('banners').select('*').eq('is_active', True).order('display_order').execute()
        banners = banners.data if banners.data else []
    except:
        banners = []
    
    # Get main categories
    categories = ProductService.get_categories()
    
    return render_template('main/index.html',
                         featured_products=featured_products,
                         banners=banners,
                         categories=categories)


@main_bp.route('/nosotros')
def about():
    """About us page"""
    try:
        supabase = get_supabase_client()
        page = supabase.table('pages').select('*').eq('slug', 'nosotros').eq('is_published', True).single().execute()
        page = page.data if page.data else None
    except:
        page = None
    
    return render_template('main/page.html', page=page)


@main_bp.route('/contacto')
def contact():
    """Contact page"""
    try:
        supabase = get_supabase_client()
        page = supabase.table('pages').select('*').eq('slug', 'contacto').eq('is_published', True).single().execute()
        page = page.data if page.data else None
    except:
        page = None
    
    return render_template('main/contact.html', page=page)


@main_bp.route('/terminos')
def terms():
    """Terms and conditions"""
    try:
        supabase = get_supabase_client()
        page = supabase.table('pages').select('*').eq('slug', 'terminos').eq('is_published', True).single().execute()
        page = page.data if page.data else None
    except:
        page = None
    
    return render_template('main/page.html', page=page)


@main_bp.route('/privacidad')
def privacy():
    """Privacy policy"""
    try:
        supabase = get_supabase_client()
        page = supabase.table('pages').select('*').eq('slug', 'privacidad').eq('is_published', True).single().execute()
        page = page.data if page.data else None
    except:
        page = None
    
    return render_template('main/page.html', page=page)


@main_bp.route('/devoluciones')
def returns():
    """Returns policy"""
    try:
        supabase = get_supabase_client()
        page = supabase.table('pages').select('*').eq('slug', 'devoluciones').eq('is_published', True).single().execute()
        page = page.data if page.data else None
    except:
        page = None
    
    return render_template('main/page.html', page=page)


@main_bp.route('/buscar')
def search():
    """Search page"""
    query = request.args.get('q', '')
    
    if query:
        products = ProductService.search_products(query, limit=50)
    else:
        products = []
    
    return render_template('main/search.html', query=query, products=products)


@main_bp.route('/health')
def health():
    """Health check endpoint for monitoring"""
    try:
        # Check database connection
        supabase = get_supabase_client()
        supabase.table('app_users').select('id', count='exact').limit(1).execute()
        
        return {
            'status': 'healthy',
            'service': 'La Bodegona',
            'version': '1.0.0'
        }, 200
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e)
        }, 503
