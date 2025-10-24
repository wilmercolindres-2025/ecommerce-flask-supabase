"""
Supabase Client Service
"""
import os
from typing import Optional
from supabase import create_client, Client

_supabase_client: Optional[Client] = None
_supabase_admin_client: Optional[Client] = None


def get_supabase_client() -> Client:
    """Client público (anon)"""
    global _supabase_client
    if _supabase_client is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        if not url or not key:
            raise ValueError("SUPABASE_URL y SUPABASE_ANON_KEY deben estar configurados")
        _supabase_client = create_client(url, key)
    return _supabase_client


def get_supabase_admin_client() -> Client:
    """Client admin (service role)"""
    global _supabase_admin_client
    if _supabase_admin_client is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        if not url or not key:
            raise ValueError("SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY deben estar configurados")
        _supabase_admin_client = create_client(url, key)
    return _supabase_admin_client


def get_public_url(path: str) -> str:
    """Devuelve URL pública de un archivo en el bucket 'products'"""
    client = get_supabase_client()
    return client.storage.from_("products").get_public_url(path)


def get_db_connection():
    """Conexión directa a Postgres (psycopg2)"""
    import psycopg2
    from urllib.parse import urlparse

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL debe estar configurada")

    # Render/Supabase pueden requerir SSL
    if "sslmode=" not in database_url:
        if "?" in database_url:
            database_url += "&sslmode=require"
        else:
            database_url += "?sslmode=require"

    result = urlparse(database_url)
    return psycopg2.connect(
        database=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port,
        sslmode="require",
    )
