-- =====================================================
-- Row Level Security (RLS) Policies
-- =====================================================

-- Enable RLS on all tables
ALTER TABLE app_users ENABLE ROW LEVEL SECURITY;
ALTER TABLE addresses ENABLE ROW LEVEL SECURITY;
ALTER TABLE brands ENABLE ROW LEVEL SECURITY;
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE product_variants ENABLE ROW LEVEL SECURITY;
ALTER TABLE product_images ENABLE ROW LEVEL SECURITY;
ALTER TABLE related_products ENABLE ROW LEVEL SECURITY;
ALTER TABLE inventory_movements ENABLE ROW LEVEL SECURITY;
ALTER TABLE carts ENABLE ROW LEVEL SECURITY;
ALTER TABLE cart_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE wishlists ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE order_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE payments ENABLE ROW LEVEL SECURITY;
ALTER TABLE shipping_zones ENABLE ROW LEVEL SECURITY;
ALTER TABLE shipping_rates ENABLE ROW LEVEL SECURITY;
ALTER TABLE shipments ENABLE ROW LEVEL SECURITY;
ALTER TABLE coupons ENABLE ROW LEVEL SECURITY;
ALTER TABLE coupon_usage ENABLE ROW LEVEL SECURITY;
ALTER TABLE banners ENABLE ROW LEVEL SECURITY;
ALTER TABLE pages ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

-- =====================================================
-- Helper Functions
-- =====================================================

-- Get current user's role
CREATE OR REPLACE FUNCTION get_user_role()
RETURNS user_role AS $$
BEGIN
    RETURN (
        SELECT role 
        FROM app_users 
        WHERE id = auth.uid()
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Check if user is admin
CREATE OR REPLACE FUNCTION is_admin()
RETURNS BOOLEAN AS $$
BEGIN
    RETURN get_user_role() = 'admin';
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Check if user is gestor or admin
CREATE OR REPLACE FUNCTION is_gestor_or_admin()
RETURNS BOOLEAN AS $$
BEGIN
    RETURN get_user_role() IN ('admin', 'gestor');
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- =====================================================
-- APP USERS
-- =====================================================

-- Users can read their own profile
CREATE POLICY "Users can view own profile"
    ON app_users FOR SELECT
    USING (auth.uid() = id);

-- Users can update their own profile (except role)
CREATE POLICY "Users can update own profile"
    ON app_users FOR UPDATE
    USING (auth.uid() = id)
    WITH CHECK (
        auth.uid() = id AND
        role = (SELECT role FROM app_users WHERE id = auth.uid())
    );

-- Admins can view all users
CREATE POLICY "Admins can view all users"
    ON app_users FOR SELECT
    USING (is_admin());

-- Admins can update any user
CREATE POLICY "Admins can update any user"
    ON app_users FOR UPDATE
    USING (is_admin());

-- Admins can insert users
CREATE POLICY "Admins can insert users"
    ON app_users FOR INSERT
    WITH CHECK (is_admin());

-- =====================================================
-- ADDRESSES
-- =====================================================

-- Users can manage their own addresses
CREATE POLICY "Users can view own addresses"
    ON addresses FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own addresses"
    ON addresses FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own addresses"
    ON addresses FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own addresses"
    ON addresses FOR DELETE
    USING (auth.uid() = user_id);

-- Admins can view all addresses
CREATE POLICY "Admins can view all addresses"
    ON addresses FOR SELECT
    USING (is_admin());

-- =====================================================
-- BRANDS
-- =====================================================

-- Everyone can view active brands
CREATE POLICY "Anyone can view active brands"
    ON brands FOR SELECT
    USING (is_active = true OR is_admin());

-- Only admins can manage brands
CREATE POLICY "Admins can insert brands"
    ON brands FOR INSERT
    WITH CHECK (is_admin());

CREATE POLICY "Admins can update brands"
    ON brands FOR UPDATE
    USING (is_admin());

CREATE POLICY "Admins can delete brands"
    ON brands FOR DELETE
    USING (is_admin());

-- =====================================================
-- CATEGORIES
-- =====================================================

-- Everyone can view active categories
CREATE POLICY "Anyone can view active categories"
    ON categories FOR SELECT
    USING (is_active = true OR is_admin());

-- Only admins can manage categories
CREATE POLICY "Admins can insert categories"
    ON categories FOR INSERT
    WITH CHECK (is_admin());

CREATE POLICY "Admins can update categories"
    ON categories FOR UPDATE
    USING (is_admin());

CREATE POLICY "Admins can delete categories"
    ON categories FOR DELETE
    USING (is_admin());

-- =====================================================
-- PRODUCTS
-- =====================================================

-- Everyone can view published products
CREATE POLICY "Anyone can view published products"
    ON products FOR SELECT
    USING (status = 'publicado' OR is_admin() OR is_gestor_or_admin());

-- Only admins can insert products
CREATE POLICY "Admins can insert products"
    ON products FOR INSERT
    WITH CHECK (is_admin());

-- Only admins can update products
CREATE POLICY "Admins can update products"
    ON products FOR UPDATE
    USING (is_admin());

-- Only admins can delete products
CREATE POLICY "Admins can delete products"
    ON products FOR DELETE
    USING (is_admin());

-- =====================================================
-- PRODUCT VARIANTS
-- =====================================================

-- Everyone can view variants of published products
CREATE POLICY "Anyone can view published product variants"
    ON product_variants FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM products 
            WHERE products.id = product_variants.product_id 
            AND products.status = 'publicado'
        ) OR is_admin()
    );

-- Only admins can manage variants
CREATE POLICY "Admins can insert variants"
    ON product_variants FOR INSERT
    WITH CHECK (is_admin());

CREATE POLICY "Admins can update variants"
    ON product_variants FOR UPDATE
    USING (is_admin());

CREATE POLICY "Admins can delete variants"
    ON product_variants FOR DELETE
    USING (is_admin());

-- =====================================================
-- PRODUCT IMAGES
-- =====================================================

-- Everyone can view images of published products
CREATE POLICY "Anyone can view published product images"
    ON product_images FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM products 
            WHERE products.id = product_images.product_id 
            AND products.status = 'publicado'
        ) OR is_admin()
    );

-- Only admins can manage images
CREATE POLICY "Admins can insert images"
    ON product_images FOR INSERT
    WITH CHECK (is_admin());

CREATE POLICY "Admins can update images"
    ON product_images FOR UPDATE
    USING (is_admin());

CREATE POLICY "Admins can delete images"
    ON product_images FOR DELETE
    USING (is_admin());

-- =====================================================
-- RELATED PRODUCTS
-- =====================================================

-- Everyone can view related products
CREATE POLICY "Anyone can view related products"
    ON related_products FOR SELECT
    USING (true);

-- Only admins can manage related products
CREATE POLICY "Admins can insert related products"
    ON related_products FOR INSERT
    WITH CHECK (is_admin());

CREATE POLICY "Admins can delete related products"
    ON related_products FOR DELETE
    USING (is_admin());

-- =====================================================
-- INVENTORY MOVEMENTS
-- =====================================================

-- Only admins can view inventory movements
CREATE POLICY "Admins can view inventory movements"
    ON inventory_movements FOR SELECT
    USING (is_admin());

-- Only admins can insert inventory movements
CREATE POLICY "Admins can insert inventory movements"
    ON inventory_movements FOR INSERT
    WITH CHECK (is_admin());

-- =====================================================
-- CARTS
-- =====================================================

-- Users can view their own cart
CREATE POLICY "Users can view own cart"
    ON carts FOR SELECT
    USING (auth.uid() = user_id);

-- Users can insert their own cart
CREATE POLICY "Users can insert own cart"
    ON carts FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Users can update their own cart
CREATE POLICY "Users can update own cart"
    ON carts FOR UPDATE
    USING (auth.uid() = user_id);

-- Users can delete their own cart
CREATE POLICY "Users can delete own cart"
    ON carts FOR DELETE
    USING (auth.uid() = user_id);

-- =====================================================
-- CART ITEMS
-- =====================================================

-- Users can view items in their cart
CREATE POLICY "Users can view own cart items"
    ON cart_items FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM carts 
            WHERE carts.id = cart_items.cart_id 
            AND carts.user_id = auth.uid()
        )
    );

-- Users can insert items in their cart
CREATE POLICY "Users can insert own cart items"
    ON cart_items FOR INSERT
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM carts 
            WHERE carts.id = cart_items.cart_id 
            AND carts.user_id = auth.uid()
        )
    );

-- Users can update items in their cart
CREATE POLICY "Users can update own cart items"
    ON cart_items FOR UPDATE
    USING (
        EXISTS (
            SELECT 1 FROM carts 
            WHERE carts.id = cart_items.cart_id 
            AND carts.user_id = auth.uid()
        )
    );

-- Users can delete items from their cart
CREATE POLICY "Users can delete own cart items"
    ON cart_items FOR DELETE
    USING (
        EXISTS (
            SELECT 1 FROM carts 
            WHERE carts.id = cart_items.cart_id 
            AND carts.user_id = auth.uid()
        )
    );

-- =====================================================
-- WISHLISTS
-- =====================================================

-- Users can manage their own wishlist
CREATE POLICY "Users can view own wishlist"
    ON wishlists FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own wishlist"
    ON wishlists FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own wishlist"
    ON wishlists FOR DELETE
    USING (auth.uid() = user_id);

-- =====================================================
-- ORDERS
-- =====================================================

-- Users can view their own orders
CREATE POLICY "Users can view own orders"
    ON orders FOR SELECT
    USING (auth.uid() = user_id);

-- Users can insert their own orders
CREATE POLICY "Users can insert own orders"
    ON orders FOR INSERT
    WITH CHECK (auth.uid() = user_id OR user_id IS NULL);

-- Admins can view all orders
CREATE POLICY "Admins can view all orders"
    ON orders FOR SELECT
    USING (is_admin());

-- Admins can update any order
CREATE POLICY "Admins can update any order"
    ON orders FOR UPDATE
    USING (is_admin());

-- =====================================================
-- ORDER ITEMS
-- =====================================================

-- Users can view items in their orders
CREATE POLICY "Users can view own order items"
    ON order_items FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM orders 
            WHERE orders.id = order_items.order_id 
            AND orders.user_id = auth.uid()
        ) OR is_admin()
    );

-- System can insert order items (via service role)
CREATE POLICY "System can insert order items"
    ON order_items FOR INSERT
    WITH CHECK (true);

-- =====================================================
-- PAYMENTS
-- =====================================================

-- Users can view payments for their orders
CREATE POLICY "Users can view own payments"
    ON payments FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM orders 
            WHERE orders.id = payments.order_id 
            AND orders.user_id = auth.uid()
        ) OR is_admin()
    );

-- System can manage payments (via service role)
CREATE POLICY "System can insert payments"
    ON payments FOR INSERT
    WITH CHECK (true);

CREATE POLICY "System can update payments"
    ON payments FOR UPDATE
    USING (true);

-- =====================================================
-- SHIPPING
-- =====================================================

-- Everyone can view active shipping zones and rates
CREATE POLICY "Anyone can view shipping zones"
    ON shipping_zones FOR SELECT
    USING (is_active = true OR is_admin());

CREATE POLICY "Anyone can view shipping rates"
    ON shipping_rates FOR SELECT
    USING (is_active = true OR is_admin());

-- Only admins can manage shipping
CREATE POLICY "Admins can manage shipping zones"
    ON shipping_zones FOR ALL
    USING (is_admin());

CREATE POLICY "Admins can manage shipping rates"
    ON shipping_rates FOR ALL
    USING (is_admin());

-- Users can view shipments for their orders
CREATE POLICY "Users can view own shipments"
    ON shipments FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM orders 
            WHERE orders.id = shipments.order_id 
            AND orders.user_id = auth.uid()
        ) OR is_admin()
    );

-- Admins can manage shipments
CREATE POLICY "Admins can manage shipments"
    ON shipments FOR ALL
    USING (is_admin());

-- =====================================================
-- COUPONS
-- =====================================================

-- Everyone can view active coupons (for validation)
CREATE POLICY "Anyone can view active coupons"
    ON coupons FOR SELECT
    USING (is_active = true OR is_admin());

-- Only admins can manage coupons
CREATE POLICY "Admins can manage coupons"
    ON coupons FOR ALL
    USING (is_admin());

-- Users can view their coupon usage
CREATE POLICY "Users can view own coupon usage"
    ON coupon_usage FOR SELECT
    USING (auth.uid() = user_id OR is_admin());

-- System can insert coupon usage
CREATE POLICY "System can insert coupon usage"
    ON coupon_usage FOR INSERT
    WITH CHECK (true);

-- =====================================================
-- BANNERS
-- =====================================================

-- Everyone can view active banners
CREATE POLICY "Anyone can view active banners"
    ON banners FOR SELECT
    USING (
        is_active = true AND
        (valid_from IS NULL OR valid_from <= NOW()) AND
        (valid_until IS NULL OR valid_until >= NOW())
        OR is_admin()
    );

-- Only admins can manage banners
CREATE POLICY "Admins can manage banners"
    ON banners FOR ALL
    USING (is_admin());

-- =====================================================
-- PAGES
-- =====================================================

-- Everyone can view published pages
CREATE POLICY "Anyone can view published pages"
    ON pages FOR SELECT
    USING (is_published = true OR is_admin());

-- Only admins can manage pages
CREATE POLICY "Admins can manage pages"
    ON pages FOR ALL
    USING (is_admin());

-- =====================================================
-- AUDIT LOGS
-- =====================================================

-- Users can view their own audit logs
CREATE POLICY "Users can view own audit logs"
    ON audit_logs FOR SELECT
    USING (auth.uid() = user_id OR is_admin());

-- System can insert audit logs
CREATE POLICY "System can insert audit logs"
    ON audit_logs FOR INSERT
    WITH CHECK (true);

-- Admins can view all audit logs
CREATE POLICY "Admins can view all audit logs"
    ON audit_logs FOR SELECT
    USING (is_admin());
