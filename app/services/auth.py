"""
Authentication Service
"""
from flask import session, g
from app.services.supabase import get_supabase_client, get_supabase_admin_client
from functools import wraps
from flask import redirect, url_for, flash


class AuthService:
    """Handle authentication with Supabase Auth"""
    
    @staticmethod
    def sign_up(email: str, password: str, full_name: str = None):
        """Register a new user"""
        try:
            supabase = get_supabase_client()
            
            # Sign up with Supabase Auth
            response = supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "full_name": full_name
                    }
                }
            })
            
            if response.user:
                # Create user profile in app_users
                admin_client = get_supabase_admin_client()
                admin_client.table('app_users').insert({
                    'id': response.user.id,
                    'email': email,
                    'full_name': full_name,
                    'role': 'cliente'
                }).execute()
                
                return {'success': True, 'user': response.user}
            
            return {'success': False, 'error': 'Failed to create user'}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def sign_in(email: str, password: str):
        """Sign in user"""
        try:
            supabase = get_supabase_client()
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user and response.session:
                # Store session
                session['access_token'] = response.session.access_token
                session['refresh_token'] = response.session.refresh_token
                session['user_id'] = response.user.id
                
                # Get user profile
                user_profile = AuthService.get_user_profile(response.user.id)
                if user_profile:
                    session['user_role'] = user_profile.get('role', 'cliente')
                    session['user_name'] = user_profile.get('full_name', email)
                
                return {'success': True, 'user': response.user}
            
            return {'success': False, 'error': 'Invalid credentials'}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def sign_out():
        """Sign out user"""
        try:
            supabase = get_supabase_client()
            supabase.auth.sign_out()
            
            # Clear session
            session.clear()
            
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_current_user():
        """Get current authenticated user"""
        user_id = session.get('user_id')
        if not user_id:
            return None
        
        return AuthService.get_user_profile(user_id)
    
    @staticmethod
    def get_user_profile(user_id: str):
        """Get user profile from app_users"""
        try:
            admin_client = get_supabase_admin_client()
            response = admin_client.table('app_users').select('*').eq('id', user_id).single().execute()
            return response.data if response.data else None
        except:
            return None
    
    @staticmethod
    def is_authenticated():
        """Check if user is authenticated"""
        return 'user_id' in session
    
    @staticmethod
    def is_admin():
        """Check if current user is admin"""
        return session.get('user_role') == 'admin'
    
    @staticmethod
    def is_gestor_or_admin():
        """Check if current user is gestor or admin"""
        role = session.get('user_role')
        return role in ['admin', 'gestor']
    
    @staticmethod
    def reset_password_request(email: str):
        """Request password reset"""
        try:
            supabase = get_supabase_client()
            supabase.auth.reset_password_for_email(email)
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def update_password(new_password: str):
        """Update user password"""
        try:
            supabase = get_supabase_client()
            response = supabase.auth.update_user({
                "password": new_password
            })
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}


def login_required(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not AuthService.is_authenticated():
            flash('Por favor inicia sesión para continuar', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not AuthService.is_authenticated():
            flash('Por favor inicia sesión para continuar', 'warning')
            return redirect(url_for('auth.login'))
        
        if not AuthService.is_admin():
            flash('No tienes permisos para acceder a esta página', 'error')
            return redirect(url_for('main.index'))
        
        return f(*args, **kwargs)
    return decorated_function


def gestor_or_admin_required(f):
    """Decorator to require gestor or admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not AuthService.is_authenticated():
            flash('Por favor inicia sesión para continuar', 'warning')
            return redirect(url_for('auth.login'))
        
        if not AuthService.is_gestor_or_admin():
            flash('No tienes permisos para acceder a esta página', 'error')
            return redirect(url_for('main.index'))
        
        return f(*args, **kwargs)
    return decorated_function
