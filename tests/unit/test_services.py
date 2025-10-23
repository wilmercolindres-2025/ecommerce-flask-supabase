"""
Unit tests for services
"""
import pytest
from app.services.products import ProductService
from app.services.cart import CartService


class TestProductService:
    """Test ProductService"""
    
    def test_get_products(self):
        """Test getting products"""
        products = ProductService.get_products(limit=10)
        assert isinstance(products, list)
    
    def test_get_categories(self):
        """Test getting categories"""
        categories = ProductService.get_categories()
        assert isinstance(categories, list)
    
    def test_get_brands(self):
        """Test getting brands"""
        brands = ProductService.get_brands()
        assert isinstance(brands, list)


class TestCartService:
    """Test CartService"""
    
    def test_get_cart_count(self):
        """Test getting cart count"""
        count = CartService.get_cart_count()
        assert isinstance(count, int)
        assert count >= 0
