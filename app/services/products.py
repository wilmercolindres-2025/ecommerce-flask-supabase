"""
Products Service
"""
from app.services.supabase import get_supabase_client, get_supabase_admin_client
from typing import List, Dict, Optional


class ProductService:
    """Handle product operations"""
    
    @staticmethod
    def get_products(
        category_id: str = None,
        brand_id: str = None,
        search: str = None,
        min_price: float = None,
        max_price: float = None,
        is_featured: bool = None,
        status: str = 'publicado',
        order_by: str = 'created_at',
        order_dir: str = 'desc',
        limit: int = 20,
        offset: int = 0
    ):
        """Get products with filters"""
        try:
            supabase = get_supabase_client()
            query = supabase.table('products').select(
                '*, category:categories(*), brand:brands(*), variants:product_variants(*), images:product_images(*)'
            )
            
            # Apply filters
            if status:
                query = query.eq('status', status)
            
            if category_id:
                query = query.eq('category_id', category_id)
            
            if brand_id:
                query = query.eq('brand_id', brand_id)
            
            if search:
                query = query.ilike('name', f'%{search}%')
            
            if min_price is not None:
                query = query.gte('base_price', min_price)
            
            if max_price is not None:
                query = query.lte('base_price', max_price)
            
            if is_featured is not None:
                query = query.eq('is_featured', is_featured)
            
            # Order
            if order_dir == 'asc':
                query = query.order(order_by, desc=False)
            else:
                query = query.order(order_by, desc=True)
            
            # Pagination
            query = query.range(offset, offset + limit - 1)
            
            response = query.execute()
            return response.data if response.data else []
        
        except Exception as e:
            print(f"Error getting products: {e}")
            return []
    
    @staticmethod
    def get_product_by_id(product_id: str):
        """Get product by ID"""
        try:
            supabase = get_supabase_client()
            response = supabase.table('products').select(
                '*, category:categories(*), brand:brands(*), variants:product_variants(*), images:product_images(*)'
            ).eq('id', product_id).single().execute()
            
            return response.data if response.data else None
        except Exception as e:
            print(f"Error getting product: {e}")
            return None
    
    @staticmethod
    def get_product_by_slug(slug: str):
        """Get product by slug"""
        try:
            supabase = get_supabase_client()
            response = supabase.table('products').select(
                '*, category:categories(*), brand:brands(*), variants:product_variants(*), images:product_images(*)'
            ).eq('slug', slug).eq('status', 'publicado').single().execute()
            
            return response.data if response.data else None
        except Exception as e:
            print(f"Error getting product: {e}")
            return None
    
    @staticmethod
    def get_featured_products(limit: int = 8):
        """Get featured products"""
        return ProductService.get_products(
            is_featured=True,
            status='publicado',
            limit=limit
        )
    
    @staticmethod
    def get_related_products(product_id: str, limit: int = 4):
        """Get related products"""
        try:
            supabase = get_supabase_client()
            response = supabase.table('related_products').select(
                'related_product:products!related_product_id(*, images:product_images(*))'
            ).eq('product_id', product_id).limit(limit).execute()
            
            if response.data:
                return [item['related_product'] for item in response.data if item.get('related_product')]
            return []
        except Exception as e:
            print(f"Error getting related products: {e}")
            return []
    
    @staticmethod
    def create_product(data: Dict, user_id: str):
        """Create new product (admin only)"""
        try:
            admin_client = get_supabase_admin_client()
            
            # Add creator
            data['created_by'] = user_id
            data['updated_by'] = user_id
            
            response = admin_client.table('products').insert(data).execute()
            return {'success': True, 'data': response.data[0] if response.data else None}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def update_product(product_id: str, data: Dict, user_id: str):
        """Update product (admin only)"""
        try:
            admin_client = get_supabase_admin_client()
            
            # Add updater
            data['updated_by'] = user_id
            
            response = admin_client.table('products').update(data).eq('id', product_id).execute()
            return {'success': True, 'data': response.data[0] if response.data else None}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def delete_product(product_id: str):
        """Delete product (admin only)"""
        try:
            admin_client = get_supabase_admin_client()
            admin_client.table('products').delete().eq('id', product_id).execute()
            return {'success': True}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_categories(parent_id: str = None, is_active: bool = True):
        """Get categories"""
        try:
            supabase = get_supabase_client()
            query = supabase.table('categories').select('*')
            
            if parent_id is not None:
                query = query.eq('parent_id', parent_id)
            else:
                query = query.is_('parent_id', 'null')
            
            if is_active:
                query = query.eq('is_active', True)
            
            query = query.order('display_order')
            
            response = query.execute()
            return response.data if response.data else []
        
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []
    
    @staticmethod
    def get_category_by_slug(slug: str):
        """Get category by slug"""
        try:
            supabase = get_supabase_client()
            response = supabase.table('categories').select('*').eq('slug', slug).single().execute()
            return response.data if response.data else None
        except Exception as e:
            print(f"Error getting category: {e}")
            return None
    
    @staticmethod
    def get_brands(is_active: bool = True):
        """Get brands"""
        try:
            supabase = get_supabase_client()
            query = supabase.table('brands').select('*')
            
            if is_active:
                query = query.eq('is_active', True)
            
            query = query.order('name')
            
            response = query.execute()
            return response.data if response.data else []
        
        except Exception as e:
            print(f"Error getting brands: {e}")
            return []
    
    @staticmethod
    def search_products(query: str, limit: int = 20):
        """Search products by name or SKU"""
        try:
            supabase = get_supabase_client()
            response = supabase.table('products').select(
                '*, category:categories(*), brand:brands(*), images:product_images(*)'
            ).or_(
                f'name.ilike.%{query}%,sku.ilike.%{query}%'
            ).eq('status', 'publicado').limit(limit).execute()
            
            return response.data if response.data else []
        
        except Exception as e:
            print(f"Error searching products: {e}")
            return []
