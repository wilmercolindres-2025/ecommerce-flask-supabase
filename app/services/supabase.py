"""
Supabase Client Service
"""

import os
from typing import Optional, Dict, Any
from supabase import create_client, Client


# Caché de clientes
_supabase_client: Optional[Client] = None
_supabase_admin_client: Optional[Client] = None


def _required_env(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise ValueError(f"{name} must be set")
    return val


def get_supabase_client() -> Client:
    """
    Devuelve cliente Supabase con ANON KEY (operaciones públicas).
    Cachea la instancia para evitar recrearla por request.
    """
    global _supabase_client
    if _supabase_client is None:
        url = _required_env("SUPABASE_URL")
        key = _required_env("SUPABASE_ANON_KEY")
        # create_client moderno: NO usar argumentos como 'proxy'
        _supabase_client = create_client(url, key)
    return _supabase_client


def get_supabase_admin_client() -> Client:
    """
    Devuelve cliente Supabase con SERVICE ROLE KEY (operaciones administrativas).
    """
    global _supabase_admin_client
    if _supabase_admin_client is None:
        url = _required_env("SUPABASE_URL")
        key = _required_env("SUPABASE_SERVICE_ROLE_KEY")
        _supabase_admin_client = create_client(url, key)
    return _supabase_admin_client


def reset_supabase_clients() -> None:
    """
    Permite limpiar el caché si rotas llaves/URL en runtime (poco común).
    """
    global _supabase_client, _supabase_admin_client
    _supabase_client = None
    _supabase_admin_client = None


def get_db_connection():
    """
    Conexión directa a la base usando psycopg2.
    - Si DATABASE_URL no incluye sslmode, forzamos sslmode='require' (útil para Supabase).
    """
    import psycopg2
    from urllib.parse import urlparse, parse_qsl

    database_url = _required_env("DATABASE_URL")

    # Parse DSN
    parsed = urlparse(database_url)
    qs: Dict[str, Any] = dict(parse_qsl(parsed.query))

    # Forzar SSL si no está presente
    qs.setdefault("sslmode", "require")

    conn = psycopg2.connect(
        dbname=parsed.path[1:],  # strip leading '/'
        user=parsed.username,
        password=parsed.password,
        host=parsed.hostname,
        port=parsed.port,
        **qs,  # incluye sslmode=require u otros params del query string
    )
    return conn


class SupabaseService:
    """Base service class para operaciones con Supabase y/o SQL directo."""

    def __init__(self, use_admin: bool = False):
        self.client = get_supabase_admin_client() if use_admin else get_supabase_client()

    def execute_query(self, query: str, params: tuple = None):
        """
        Ejecuta SQL crudo (usar con responsabilidad).
        - Retorna lista de dicts si es SELECT.
        - Para otras operaciones, hace COMMIT y retorna rowcount.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            is_select = query.lstrip().upper().startswith("SELECT")
            if is_select:
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in rows]
            else:
                conn.commit()
                return cursor.rowcount
        finally:
            cursor.close()
            conn.close()
