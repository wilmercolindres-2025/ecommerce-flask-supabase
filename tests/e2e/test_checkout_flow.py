"""
End-to-end tests for checkout flow
"""
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
class TestCheckoutFlow:
    """Test complete checkout flow"""
    
    def test_add_to_cart_and_checkout(self, page: Page):
        """Test adding product to cart and completing checkout"""
        # Navigate to home
        page.goto('http://localhost:5000')
        
        # Wait for page to load
        expect(page.locator('h1')).to_contain_text('Mi Tienda GT')
        
        # Click on first product
        page.locator('.product-card').first.click()
        
        # Add to cart
        page.locator('button:has-text("Agregar al Carrito")').click()
        
        # Wait for success message
        expect(page.locator('.alert-success')).to_be_visible()
        
        # Go to cart
        page.goto('http://localhost:5000/carrito/')
        
        # Verify cart has items
        expect(page.locator('.cart-item')).to_have_count(1)
        
        # Proceed to checkout
        page.locator('a:has-text("Proceder al Pago")').click()
        
        # Fill customer info
        page.fill('input[name="name"]', 'Test User')
        page.fill('input[name="email"]', 'test@example.com')
        page.fill('input[name="phone"]', '12345678')
        
        # Continue to shipping
        page.locator('button:has-text("Continuar")').click()
        
        # Fill shipping info
        page.fill('input[name="address_line1"]', 'Test Address 123')
        page.fill('input[name="city"]', 'Guatemala')
        page.select_option('select[name="state"]', 'Guatemala')
        
        # Continue to review
        page.locator('button:has-text("Continuar")').click()
        
        # Confirm order
        page.locator('button:has-text("Confirmar Pedido")').click()
        
        # Verify success page
        expect(page.locator('h1')).to_contain_text('¡Pedido Exitoso!')
