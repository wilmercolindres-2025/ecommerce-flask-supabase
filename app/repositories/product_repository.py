# app/repositories/product_repository.py
from typing import Any, Dict, List, Optional
from supabase import Client
from app.services.supabase_service import get_supabase_client, get_public_url


class ProductRepository:
    def __init__(self, client: Optional[Client] = None) -> None:
        self.client: Client = client or get_supabase_client()

    # ---------- Productos ----------
    def get_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        # Tabla: products (según tu schema)
        resp = (
            self.client.table("products")
            .select(
                "id, sku, name, slug, short_description, description, technical_specs, "
                "base_price, sale_price, status, category_id, brand_id"
            )
            .eq("slug", slug)
            .limit(1)
            .execute()
        )
        items = resp.data or []
        if not items:
            return None

        product = items[0]

        # Enriquecer con marca/categoría (opcionales)
        product["brand"] = self._get_brand(product.get("brand_id"))
        product["category"] = self._get_category(product.get("category_id"))
        return product

    # ---------- Imágenes ----------
    def get_images(self, product_id: str) -> List[Dict[str, Any]]:
        resp = (
            self.client.table("product_images")
            .select("id, storage_path, alt_text, is_primary, display_order")
            .eq("product_id", product_id)
            .order("is_primary", desc=True)
            .order("display_order", asc=True)
            .execute()
        )
        rows = resp.data or []
        images: List[Dict[str, Any]] = []
        for r in rows:
            path = r.get("storage_path")
            images.append(
                {
                    "id": r.get("id"),
                    "url": get_public_url(path) if path else None,  # ← URL pública del bucket
                    "alt_text": r.get("alt_text"),
                    "is_primary": r.get("is_primary"),
                    "display_order": r.get("display_order"),
                }
            )
        return images

    # ---------- Variantes ----------
    def get_variants(self, product_id: str) -> List[Dict[str, Any]]:
        resp = (
            self.client.table("product_variants")
            .select("id, name, attributes, price_adjustment, stock, is_active")
            .eq("product_id", product_id)
            .order("created_at", asc=True)
            .execute()
        )
        return resp.data or []

    # ---------- Relacionados (opcional) ----------
    def get_related(self, product_id: str, limit: int = 8) -> List[Dict[str, Any]]:
        # Usa related_products si la tienes, o fallback: misma categoría
        # 1) intento por tabla related_products
        rel = (
            self.client.table("related_products")
            .select("related_product_id")
            .eq("product_id", product_id)
            .limit(limit)
            .execute()
        )
        ids = [r["related_product_id"] for r in (rel.data or []) if r.get("related_product_id")]

        if ids:
            resp = (
                self.client.table("products")
                .select("id, name, slug, base_price, sale_price")
                .in_("id", ids)
                .limit(limit)
                .execute()
            )
            products = resp.data or []
        else:
            # fallback: mismos de la misma categoría (excluyendo el mismo producto)
            prod = (
                self.client.table("products")
                .select("category_id")
                .eq("id", product_id)
                .limit(1)
                .execute()
            )
            cat_id = (prod.data or [{}])[0].get("category_id")
            if not cat_id:
                return []
            resp = (
                self.client.table("products")
                .select("id, name, slug, base_price, sale_price")
                .eq("category_id", cat_id)
                .neq("id", product_id)
                .limit(limit)
                .execute()
            )
            products = resp.data or []

        # Adjunta primera imagen (si existe)
        out: List[Dict[str, Any]] = []
        for p in products:
            imgs = (
                self.client.table("product_images")
                .select("storage_path")
                .eq("product_id", p["id"])
                .order("is_primary", desc=True)
                .order("display_order", asc=True)
                .limit(1)
                .execute()
            )
            first = (imgs.data or [{}])[0].get("storage_path")
            p["images"] = [{"url": get_public_url(first)}] if first else []
            out.append(p)
        return out

    # ---------- Helpers internos ----------
    def _get_brand(self, brand_id: Optional[str]) -> Optional[Dict[str, Any]]:
        if not brand_id:
            return None
        resp = (
            self.client.table("brands")
            .select("id, name, slug")
            .eq("id", brand_id)
            .limit(1)
            .execute()
        )
        items = resp.data or []
        return items[0] if items else None

    def _get_category(self, category_id: Optional[str]) -> Optional[Dict[str, Any]]:
        if not category_id:
            return None
        resp = (
            self.client.table("categories")
            .select("id, name, slug")
            .eq("id", category_id)
            .limit(1)
            .execute()
        )
        items = resp.data or []
        return items[0] if items else None
