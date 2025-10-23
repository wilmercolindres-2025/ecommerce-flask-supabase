"""
Integration tests for routes
"""
import pytest


class TestMainRoutes:
    """Test main routes"""
    
    def test_home_page(self, client):
        """Test home page loads"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Mi Tienda GT' in response.data
    
    def test_catalog_page(self, client):
        """Test catalog page loads"""
        response = client.get('/catalogo/')
        assert response.status_code == 200
    
    def test_search_page(self, client):
        """Test search page"""
        response = client.get('/buscar?q=laptop')
        assert response.status_code == 200


class TestAuthRoutes:
    """Test authentication routes"""
    
    def test_login_page(self, client):
        """Test login page loads"""
        response = client.get('/auth/login')
        assert response.status_code == 200
    
    def test_register_page(self, client):
        """Test register page loads"""
        response = client.get('/auth/registro')
        assert response.status_code == 200


class TestCartRoutes:
    """Test cart routes"""
    
    def test_cart_page(self, client):
        """Test cart page loads"""
        response = client.get('/carrito/')
        assert response.status_code == 200
    
    def test_cart_count(self, client):
        """Test cart count endpoint"""
        response = client.get('/carrito/contador')
        assert response.status_code == 200
        assert response.json is not None
