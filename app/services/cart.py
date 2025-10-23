"""
Shopping Cart Service
"""
from flask import session
from app.services.supabase import get_supabase_client, get_supabase_admin_client
from app.services.auth import AuthService
from typing import Dict, List
import uuid


class CartService:
    """Handle shopping cart operations"""
    
    @staticmethod
    def get_or_create_cart():
        """Get or create cart for current user/session"""
        try:
            user_id = session.get('user_id')
            
            if user_id:
                # Authenticated user
                supabase = get_supabase_admin_client()
                response = supabase.table('carts').select('*').eq('user_id', user_id).execute()
                
                if response.data and len(response.data) > 0:
                    return response.data[0]
                else:
                    # Create new cart
                    new_cart = supabase.table('carts').insert({
                        'user_id': user_id
                    }).execute()
                    return new_cart.data[0] if new_cart.data else None
            else:
                # Guest user - use session
                session_id = session.get('cart_session_id')
                
                if not session_id:
                    session_id = str(uuid.uuid4())
                    session['cart_session_id'] = session_id
                
                supabase = get_supabase_admin_client()
                response = supabase.table('carts').select('*').eq('session_id', session_id).execute()
                
                if response.data and len(response.data) > 0:
                    return response.data[0]
                else:
                    # Create new cart
                    new_cart = supabase.table('carts').insert({
                        'session_id': session_id
                    }).execute()
                    return new_cart.data[0] if new_cart.data else None
        
        except Exception as e:
            print(f"Error getting/creating cart: {e}")
            return None
    
    @staticmethod
    def get_cart_items():
        """Get all items in cart"""
        try:
            cart = CartService.get_or_create_cart()
            if not cart:
                return []
            
            supabase = get_supabase_admin_client()
            response = supabase.table('cart_items').select(
                '*, product:products(*, images:product_images(*)), variant:product_variants(*)'
            ).eq('cart_id', cart['id']).execute()
            
            return response.data if response.data else []
        
        except Exception as e:
            print(f"Error getting cart items: {e}")
            return []
    
    @staticmethod
    def add_to_cart(product_id: str, variant_id: str = None, quantity: int = 1):
        """Add item to cart"""
        try:
            cart = CartService.get_or_create_cart()
            if not cart:
                return {'success': False, 'error': 'Could not create cart'}
            
            supabase = get_supabase_admin_client()
            
            # Get product price
            product = supabase.table('products').select('base_price, sale_price').eq('id', product_id).single().execute()
            if not product.data:
                return {'success': False, 'error': 'Product not found'}
            
            price = product.data.get('sale_price') or product.data.get('base_price')
            
            # Check if item already exists
            query = supabase.table('cart_items').select('*').eq('cart_id', cart['id']).eq('product_id', product_id)
            if variant_id:
                query = query.eq('variant_id', variant_id)
            else:
                query = query.is_('variant_id', 'null')
            
            existing = query.execute()
            
            if existing.data and len(existing.data) > 0:
                # Update quantity
                item = existing.data[0]
                new_quantity = item['quantity'] + quantity
                supabase.table('cart_items').update({
                    'quantity': new_quantity
                }).eq('id', item['id']).execute()
            else:
                # Add new item
                supabase.table('cart_items').insert({
                    'cart_id': cart['id'],
                    'product_id': product_id,
                    'variant_id': variant_id,
                    'quantity': quantity,
                    'price': price
                }).execute()
            
            return {'success': True}
        
        except Exception as e:
            print(f"Error adding to cart: {e}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def update_cart_item(item_id: str, quantity: int):
        """Update cart item quantity"""
        try:
            if quantity <= 0:
                return CartService.remove_from_cart(item_id)
            
            supabase = get_supabase_admin_client()
            supabase.table('cart_items').update({
                'quantity': quantity
            }).eq('id', item_id).execute()
            
            return {'success': True}
        
        except Exception as e:
            print(f"Error updating cart item: {e}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def remove_from_cart(item_id: str):
        """Remove item from cart"""
        try:
            supabase = get_supabase_admin_client()
            supabase.table('cart_items').delete().eq('id', item_id).execute()
            return {'success': True}
        
        except Exception as e:
            print(f"Error removing from cart: {e}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def clear_cart():
        """Clear all items from cart"""
        try:
            cart = CartService.get_or_create_cart()
            if not cart:
                return {'success': False, 'error': 'Cart not found'}
            
            supabase = get_supabase_admin_client()
            supabase.table('cart_items').delete().eq('cart_id', cart['id']).execute()
            
            return {'success': True}
        
        except Exception as e:
            print(f"Error clearing cart: {e}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_cart_total():
        """Calculate cart total"""
        items = CartService.get_cart_items()
        total = sum(float(item['price']) * item['quantity'] for item in items)
        return total
    
    @staticmethod
    def get_cart_count():
        """Get total number of items in cart"""
        items = CartService.get_cart_items()
        return sum(item['quantity'] for item in items)
    
    @staticmethod
    def merge_guest_cart(user_id: str):
        """Merge guest cart with user cart after login"""
        try:
            session_id = session.get('cart_session_id')
            if not session_id:
                return
            
            supabase = get_supabase_admin_client()
            
            # Get guest cart
            guest_cart = supabase.table('carts').select('*').eq('session_id', session_id).execute()
            if not guest_cart.data:
                return
            
            # Get or create user cart
            user_cart = supabase.table('carts').select('*').eq('user_id', user_id).execute()
            if not user_cart.data:
                # Create user cart
                user_cart = supabase.table('carts').insert({'user_id': user_id}).execute()
            
            if not user_cart.data:
                return
            
            # Move items from guest cart to user cart
            guest_items = supabase.table('cart_items').select('*').eq('cart_id', guest_cart.data[0]['id']).execute()
            
            if guest_items.data:
                for item in guest_items.data:
                    # Check if item exists in user cart
                    existing = supabase.table('cart_items').select('*').eq(
                        'cart_id', user_cart.data[0]['id']
                    ).eq('product_id', item['product_id'])
                    
                    if item.get('variant_id'):
                        existing = existing.eq('variant_id', item['variant_id'])
                    
                    existing = existing.execute()
                    
                    if existing.data:
                        # Update quantity
                        new_qty = existing.data[0]['quantity'] + item['quantity']
                        supabase.table('cart_items').update({
                            'quantity': new_qty
                        }).eq('id', existing.data[0]['id']).execute()
                    else:
                        # Add item
                        supabase.table('cart_items').insert({
                            'cart_id': user_cart.data[0]['id'],
                            'product_id': item['product_id'],
                            'variant_id': item.get('variant_id'),
                            'quantity': item['quantity'],
                            'price': item['price']
                        }).execute()
            
            # Delete guest cart
            supabase.table('cart_items').delete().eq('cart_id', guest_cart.data[0]['id']).execute()
            supabase.table('carts').delete().eq('id', guest_cart.data[0]['id']).execute()
            
            # Clear session
            session.pop('cart_session_id', None)
        
        except Exception as e:
            print(f"Error merging carts: {e}")


def get_cart_count():
    """Helper function for template context"""
    try:
        return CartService.get_cart_count()
    except:
        return 0
