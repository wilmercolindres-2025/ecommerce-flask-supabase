"""
Supabase Client Service
"""
import os
from supabase import create_client, Client
from typing import Optional
from app.services.supabase import get_supabase_client, get_public_url

_supabase_client: Optional[Client] = None
_supabase_admin_client: Optional[Client] = None


def get_supabase_client() -> Client:
    """Get Supabase client with anon key (for public operations)"""
    global _supabase_client
    
    if _supabase_client is None:
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_ANON_KEY')
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")
        
        _supabase_client = create_client(url, key)
    
    return _supabase_client


def get_supabase_admin_client() -> Client:
    """Get Supabase client with service role key (for admin operations)"""
    global _supabase_admin_client
    
    if _supabase_admin_client is None:
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
        
        _supabase_admin_client = create_client(url, key)
    
    return _supabase_admin_client


def get_db_connection():
    """Get direct database connection using psycopg2"""
    import psycopg2
    from urllib.parse import urlparse
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL must be set")
    
    # Parse the database URL
    result = urlparse(database_url)
    
    conn = psycopg2.connect(
        database=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )
    
    return conn


class SupabaseService:
    """Base service class for Supabase operations"""
    
    def __init__(self, use_admin=False):
        self.client = get_supabase_admin_client() if use_admin else get_supabase_client()
    
    def execute_query(self, query: str, params: tuple = None):
        """Execute raw SQL query"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in result]
            else:
                conn.commit()
                return cursor.rowcount
        finally:
            cursor.close()
            conn.close()



class ProductService:
    # ... tus métodos existentes ...

    @staticmethod
    def get_product_images(product_id: str):
        supabase = get_supabase_client()
        resp = (
            supabase.table('product_images')
            .select('id, storage_path, alt_text, is_primary, display_order')
            .eq('product_id', product_id)
            .order('is_primary', desc=True)
            .order('display_order', asc=True)
            .execute()
        )
        rows = resp.data or []
        out = []
        for r in rows:
            path = r.get('storage_path')
            out.append({
                'id': r.get('id'),
                'url': get_public_url(path) if path else None,
                'alt_text': r.get('alt_text'),
                'is_primary': r.get('is_primary'),
                'display_order': r.get('display_order'),
            })
        return out

    @staticmethod
    def get_product_variants(product_id: str):
        supabase = get_supabase_client()
        resp = (
            supabase.table('product_variants')
            .select('id, name, attributes, price_adjustment, stock, is_active')
            .eq('product_id', product_id)
            .order('created_at', asc=True)
            .execute()
        )
        return resp.data or []

