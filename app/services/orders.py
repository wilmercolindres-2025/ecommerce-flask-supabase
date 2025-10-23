"""
Orders Service
"""
from app.services.supabase import get_supabase_admin_client
from app.services.cart import CartService
from typing import Dict
import uuid
from datetime import datetime


class OrderService:
    """Handle order operations"""
    
    @staticmethod
    def create_order(order_data: Dict):
        """Create new order from cart"""
        try:
            supabase = get_supabase_admin_client()
            
            # Get cart items
            cart_items = CartService.get_cart_items()
            if not cart_items:
                return {'success': False, 'error': 'Cart is empty'}
            
            # Calculate totals
            subtotal = sum(float(item['price']) * item['quantity'] for item in cart_items)
            tax_amount = order_data.get('tax_amount', 0)
            shipping_amount = order_data.get('shipping_amount', 0)
            discount_amount = order_data.get('discount_amount', 0)
            total = subtotal + tax_amount + shipping_amount - discount_amount
            
            # Generate order number
            order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
            
            # Create order
            order = {
                'order_number': order_number,
                'user_id': order_data.get('user_id'),
                'status': 'nuevo',
                'customer_email': order_data['customer_email'],
                'customer_name': order_data['customer_name'],
                'customer_phone': order_data['customer_phone'],
                'shipping_address_line1': order_data['shipping_address_line1'],
                'shipping_address_line2': order_data.get('shipping_address_line2'),
                'shipping_city': order_data['shipping_city'],
                'shipping_state': order_data['shipping_state'],
                'shipping_municipality': order_data.get('shipping_municipality'),
                'shipping_postal_code': order_data.get('shipping_postal_code'),
                'shipping_country': order_data.get('shipping_country', 'GT'),
                'subtotal': subtotal,
                'tax_amount': tax_amount,
                'shipping_amount': shipping_amount,
                'discount_amount': discount_amount,
                'total': total,
                'shipping_method': order_data.get('shipping_method', 'delivery'),
                'shipping_notes': order_data.get('shipping_notes'),
                'payment_method': order_data.get('payment_method', 'sandbox'),
                'payment_status': 'pending',
                'coupon_code': order_data.get('coupon_code'),
                'customer_notes': order_data.get('customer_notes')
            }
            
            order_response = supabase.table('orders').insert(order).execute()
            
            if not order_response.data:
                return {'success': False, 'error': 'Failed to create order'}
            
            created_order = order_response.data[0]
            
            # Create order items and update inventory
            for item in cart_items:
                product = item['product']
                variant = item.get('variant')
                
                order_item = {
                    'order_id': created_order['id'],
                    'product_id': item['product_id'],
                    'variant_id': item.get('variant_id'),
                    'sku': variant['sku'] if variant else product['sku'],
                    'product_name': product['name'],
                    'variant_name': variant['name'] if variant else None,
                    'quantity': item['quantity'],
                    'unit_price': item['price'],
                    'tax_rate': product.get('tax_rate', 0),
                    'subtotal': float(item['price']) * item['quantity']
                }
                
                supabase.table('order_items').insert(order_item).execute()
                
                # Update inventory
                if variant:
                    # Update variant stock
                    current_stock = variant['stock']
                    new_stock = max(0, current_stock - item['quantity'])
                    
                    supabase.table('product_variants').update({
                        'stock': new_stock
                    }).eq('id', variant['id']).execute()
                    
                    # Log inventory movement
                    supabase.table('inventory_movements').insert({
                        'product_id': item['product_id'],
                        'variant_id': variant['id'],
                        'movement_type': 'sale',
                        'quantity': -item['quantity'],
                        'previous_stock': current_stock,
                        'new_stock': new_stock,
                        'reference_type': 'order',
                        'reference_id': created_order['id']
                    }).execute()
            
            # Clear cart
            CartService.clear_cart()
            
            # Create payment record
            payment = {
                'order_id': created_order['id'],
                'payment_method': order_data.get('payment_method', 'sandbox'),
                'amount': total,
                'currency': 'GTQ',
                'status': 'pending'
            }
            
            supabase.table('payments').insert(payment).execute()
            
            return {'success': True, 'order': created_order}
        
        except Exception as e:
            print(f"Error creating order: {e}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_order_by_id(order_id: str):
        """Get order by ID"""
        try:
            supabase = get_supabase_admin_client()
            response = supabase.table('orders').select(
                '*, items:order_items(*, product:products(*)), payments:payments(*), shipments:shipments(*)'
            ).eq('id', order_id).single().execute()
            
            return response.data if response.data else None
        except Exception as e:
            print(f"Error getting order: {e}")
            return None
    
    @staticmethod
    def get_order_by_number(order_number: str):
        """Get order by order number"""
        try:
            supabase = get_supabase_admin_client()
            response = supabase.table('orders').select(
                '*, items:order_items(*, product:products(*)), payments:payments(*), shipments:shipments(*)'
            ).eq('order_number', order_number).single().execute()
            
            return response.data if response.data else None
        except Exception as e:
            print(f"Error getting order: {e}")
            return None
    
    @staticmethod
    def get_user_orders(user_id: str, limit: int = 20, offset: int = 0):
        """Get orders for a user"""
        try:
            supabase = get_supabase_admin_client()
            response = supabase.table('orders').select(
                '*, items:order_items(*)'
            ).eq('user_id', user_id).order('created_at', desc=True).range(offset, offset + limit - 1).execute()
            
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting user orders: {e}")
            return []
    
    @staticmethod
    def update_order_status(order_id: str, status: str, admin_notes: str = None):
        """Update order status (admin only)"""
        try:
            supabase = get_supabase_admin_client()
            
            update_data = {'status': status}
            
            if admin_notes:
                update_data['admin_notes'] = admin_notes
            
            # Set timestamps based on status
            if status == 'pagado':
                update_data['paid_at'] = datetime.now().isoformat()
                update_data['payment_status'] = 'completed'
            elif status == 'enviado':
                update_data['shipped_at'] = datetime.now().isoformat()
            elif status == 'entregado':
                update_data['delivered_at'] = datetime.now().isoformat()
            elif status == 'cancelado':
                update_data['cancelled_at'] = datetime.now().isoformat()
            
            response = supabase.table('orders').update(update_data).eq('id', order_id).execute()
            
            # Update payment status if order is paid
            if status == 'pagado':
                supabase.table('payments').update({
                    'status': 'completed',
                    'processed_at': datetime.now().isoformat()
                }).eq('order_id', order_id).execute()
            
            return {'success': True, 'data': response.data[0] if response.data else None}
        
        except Exception as e:
            print(f"Error updating order status: {e}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_all_orders(status: str = None, limit: int = 50, offset: int = 0):
        """Get all orders (admin only)"""
        try:
            supabase = get_supabase_admin_client()
            query = supabase.table('orders').select('*, items:order_items(*)')
            
            if status:
                query = query.eq('status', status)
            
            query = query.order('created_at', desc=True).range(offset, offset + limit - 1)
            
            response = query.execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting orders: {e}")
            return []
    
    @staticmethod
    def validate_coupon(code: str, subtotal: float):
        """Validate and apply coupon"""
        try:
            supabase = get_supabase_admin_client()
            response = supabase.table('coupons').select('*').eq('code', code).eq('is_active', True).single().execute()
            
            if not response.data:
                return {'valid': False, 'error': 'Cupón no válido'}
            
            coupon = response.data
            
            # Check validity dates
            now = datetime.now()
            if coupon.get('valid_from') and datetime.fromisoformat(coupon['valid_from']) > now:
                return {'valid': False, 'error': 'Cupón aún no es válido'}
            
            if coupon.get('valid_until') and datetime.fromisoformat(coupon['valid_until']) < now:
                return {'valid': False, 'error': 'Cupón expirado'}
            
            # Check minimum purchase
            if coupon.get('min_purchase_amount') and subtotal < float(coupon['min_purchase_amount']):
                return {'valid': False, 'error': f"Compra mínima de Q{coupon['min_purchase_amount']} requerida"}
            
            # Check usage limit
            if coupon.get('usage_limit') and coupon.get('usage_count', 0) >= coupon['usage_limit']:
                return {'valid': False, 'error': 'Cupón agotado'}
            
            # Calculate discount
            if coupon['type'] == 'percentage':
                discount = subtotal * (float(coupon['value']) / 100)
                if coupon.get('max_discount_amount'):
                    discount = min(discount, float(coupon['max_discount_amount']))
            else:  # fixed_amount
                discount = float(coupon['value'])
            
            return {
                'valid': True,
                'coupon': coupon,
                'discount': discount
            }
        
        except Exception as e:
            print(f"Error validating coupon: {e}")
            return {'valid': False, 'error': 'Error al validar cupón'}
