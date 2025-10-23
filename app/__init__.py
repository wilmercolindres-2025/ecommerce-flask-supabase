"""
Flask Application Factory
"""
import os
from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions
csrf = CSRFProtect()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=os.getenv('RATELIMIT_STORAGE_URL', 'memory://')
)


def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SUPABASE_URL'] = os.getenv('SUPABASE_URL')
    app.config['SUPABASE_ANON_KEY'] = os.getenv('SUPABASE_ANON_KEY')
    app.config['SUPABASE_SERVICE_ROLE_KEY'] = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
    app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
    app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
    
    # App settings
    app.config['APP_NAME'] = os.getenv('APP_NAME', 'Mi Tienda GT')
    app.config['CURRENCY'] = os.getenv('CURRENCY', 'GTQ')
    app.config['CURRENCY_SYMBOL'] = os.getenv('CURRENCY_SYMBOL', 'Q')
    app.config['LOCALE'] = os.getenv('LOCALE', 'es_GT')
    app.config['WHATSAPP_PHONE'] = os.getenv('WHATSAPP_PHONE', '+50212345678')
    
    # Payment settings
    app.config['PAYMENT_MODE'] = os.getenv('PAYMENT_MODE', 'sandbox')
    
    # Initialize extensions
    csrf.init_app(app)
    limiter.init_app(app)
    
    # Register blueprints
    from app.blueprints.main import main_bp
    from app.blueprints.auth import auth_bp
    from app.blueprints.catalog import catalog_bp
    from app.blueprints.cart import cart_bp
    from app.blueprints.checkout import checkout_bp
    from app.blueprints.user import user_bp
    from app.blueprints.admin import admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(catalog_bp, url_prefix='/catalogo')
    app.register_blueprint(cart_bp, url_prefix='/carrito')
    app.register_blueprint(checkout_bp, url_prefix='/checkout')
    app.register_blueprint(user_bp, url_prefix='/cuenta')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Context processors
    @app.context_processor
    def inject_globals():
        from app.services.cart import get_cart_count
        return {
            'app_name': app.config['APP_NAME'],
            'currency_symbol': app.config['CURRENCY_SYMBOL'],
            'whatsapp_phone': app.config['WHATSAPP_PHONE'],
            'cart_count': get_cart_count(),
            'current_year': 2024
        }
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html'), 403
    
    # Template filters
    @app.template_filter('currency')
    def currency_filter(value):
        """Format number as currency"""
        try:
            return f"{app.config['CURRENCY_SYMBOL']}{float(value):,.2f}"
        except (ValueError, TypeError):
            return f"{app.config['CURRENCY_SYMBOL']}0.00"
    
    @app.template_filter('datetime')
    def datetime_filter(value, format='%d/%m/%Y'):
        """Format datetime"""
        if value is None:
            return ''
        return value.strftime(format)
    
    return app
