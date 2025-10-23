"""
Auth Blueprint - Authentication and user management
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.auth import AuthService
from app.services.cart import CartService
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/registro', methods=['GET', 'POST'])
def register():
    """User registration"""
    if AuthService.is_authenticated():
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        full_name = request.form.get('full_name')
        
        # Validation
        if not email or not password or not password_confirm:
            flash('Todos los campos son requeridos', 'error')
            return render_template('auth/register.html')
        
        if password != password_confirm:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('auth/register.html')
        
        if len(password) < 8:
            flash('La contraseña debe tener al menos 8 caracteres', 'error')
            return render_template('auth/register.html')
        
        # Register user
        result = AuthService.sign_up(email, password, full_name)
        
        if result['success']:
            flash('Registro exitoso. Por favor verifica tu correo electrónico.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(f'Error al registrar: {result["error"]}', 'error')
    
    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if AuthService.is_authenticated():
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'
        
        if not email or not password:
            flash('Email y contraseña son requeridos', 'error')
            return render_template('auth/login.html')
        
        # Attempt login
        result = AuthService.sign_in(email, password)
        
        if result['success']:
            # Merge guest cart if exists
            CartService.merge_guest_cart(result['user'].id)
            
            flash('Inicio de sesión exitoso', 'success')
            
            # Redirect to next page or home
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            # Redirect admin to admin panel
            if AuthService.is_admin():
                return redirect(url_for('admin.dashboard'))
            
            return redirect(url_for('main.index'))
        else:
            flash(f'Error al iniciar sesión: {result["error"]}', 'error')
    
    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    """User logout"""
    AuthService.sign_out()
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('main.index'))


@auth_bp.route('/recuperar-contrasena', methods=['GET', 'POST'])
def forgot_password():
    """Password recovery"""
    if request.method == 'POST':
        email = request.form.get('email')
        
        if not email:
            flash('El email es requerido', 'error')
            return render_template('auth/forgot_password.html')
        
        result = AuthService.reset_password_request(email)
        
        if result['success']:
            flash('Se ha enviado un correo con instrucciones para recuperar tu contraseña', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Error al solicitar recuperación de contraseña', 'error')
    
    return render_template('auth/forgot_password.html')


@auth_bp.route('/restablecer-contrasena', methods=['GET', 'POST'])
def reset_password():
    """Reset password with token"""
    if request.method == 'POST':
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        
        if not password or not password_confirm:
            flash('Todos los campos son requeridos', 'error')
            return render_template('auth/reset_password.html')
        
        if password != password_confirm:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('auth/reset_password.html')
        
        if len(password) < 8:
            flash('La contraseña debe tener al menos 8 caracteres', 'error')
            return render_template('auth/reset_password.html')
        
        result = AuthService.update_password(password)
        
        if result['success']:
            flash('Contraseña actualizada exitosamente', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Error al actualizar contraseña', 'error')
    
    return render_template('auth/reset_password.html')
