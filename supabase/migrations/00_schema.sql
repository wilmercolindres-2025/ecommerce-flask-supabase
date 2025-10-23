-- =====================================================
-- E-Commerce Schema - Supabase PostgreSQL
-- =====================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- ROLES & USERS
-- =====================================================

-- App roles enum
CREATE TYPE user_role AS ENUM ('admin', 'gestor', 'cliente');

-- App roles table
CREATE TABLE app_roles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name user_role NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User profiles (extends auth.users)
CREATE TABLE app_users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(255),
    phone VARCHAR(20),
    avatar_url TEXT,
    role user_role DEFAULT 'cliente',
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User addresses
CREATE TABLE addresses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES app_users(id) ON DELETE CASCADE,
    label VARCHAR(50), -- 'casa', 'trabajo', etc.
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    address_line1 VARCHAR(255) NOT NULL,
    address_line2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    state_department VARCHAR(100) NOT NULL, -- Departamento (Guatemala)
    municipality VARCHAR(100), -- Municipio
    postal_code VARCHAR(20),
    country VARCHAR(2) DEFAULT 'GT',
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- CATALOG
-- =====================================================

-- Brands
CREATE TABLE brands (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL UNIQUE,
    slug VARCHAR(255) NOT NULL UNIQUE,
    logo_url TEXT,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Categories (hierarchical)
CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    parent_id UUID REFERENCES categories(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    description TEXT,
    image_url TEXT,
    icon VARCHAR(50),
    display_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(parent_id, slug)
);

-- Product status enum
CREATE TYPE product_status AS ENUM ('borrador', 'pendiente', 'publicado', 'oculto');

-- Products
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sku VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL UNIQUE,
    short_description TEXT,
    description TEXT,
    technical_specs JSONB, -- Ficha técnica
    category_id UUID NOT NULL REFERENCES categories(id),
    brand_id UUID REFERENCES brands(id),
    base_price DECIMAL(10, 2) NOT NULL CHECK (base_price >= 0),
    sale_price DECIMAL(10, 2) CHECK (sale_price >= 0),
    tax_rate DECIMAL(5, 2) DEFAULT 0,
    cost DECIMAL(10, 2),
    status product_status DEFAULT 'borrador',
    is_featured BOOLEAN DEFAULT FALSE,
    published_at TIMESTAMP WITH TIME ZONE,
    meta_title VARCHAR(255),
    meta_description TEXT,
    meta_keywords TEXT,
    created_by UUID REFERENCES app_users(id),
    updated_by UUID REFERENCES app_users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Product variants (talla, color, etc.)
CREATE TABLE product_variants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    sku VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL, -- "Talla M / Color Rojo"
    attributes JSONB NOT NULL, -- {"size": "M", "color": "Rojo"}
    price_adjustment DECIMAL(10, 2) DEFAULT 0,
    stock INTEGER DEFAULT 0 CHECK (stock >= 0),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Product images
CREATE TABLE product_images (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    variant_id UUID REFERENCES product_variants(id) ON DELETE CASCADE,
    storage_path TEXT NOT NULL,
    url TEXT NOT NULL,
    alt_text VARCHAR(255),
    display_order INTEGER DEFAULT 0,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Related products
CREATE TABLE related_products (
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    related_product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    relation_type VARCHAR(50) DEFAULT 'related', -- 'related', 'upsell', 'cross-sell'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (product_id, related_product_id),
    CHECK (product_id != related_product_id)
);

-- Inventory movements
CREATE TABLE inventory_movements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID REFERENCES products(id),
    variant_id UUID REFERENCES product_variants(id),
    movement_type VARCHAR(50) NOT NULL, -- 'purchase', 'sale', 'adjustment', 'return'
    quantity INTEGER NOT NULL,
    previous_stock INTEGER NOT NULL,
    new_stock INTEGER NOT NULL,
    reference_type VARCHAR(50), -- 'order', 'manual', etc.
    reference_id UUID,
    notes TEXT,
    created_by UUID REFERENCES app_users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- SHOPPING
-- =====================================================

-- Shopping carts
CREATE TABLE carts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES app_users(id) ON DELETE CASCADE,
    session_id VARCHAR(255), -- Para usuarios no autenticados
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id),
    UNIQUE(session_id)
);

-- Cart items
CREATE TABLE cart_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cart_id UUID NOT NULL REFERENCES carts(id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES products(id),
    variant_id UUID REFERENCES product_variants(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(cart_id, product_id, variant_id)
);

-- Wishlist
CREATE TABLE wishlists (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES app_users(id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, product_id)
);

-- =====================================================
-- ORDERS
-- =====================================================

-- Order status enum
CREATE TYPE order_status AS ENUM ('nuevo', 'pagado', 'procesando', 'enviado', 'entregado', 'cancelado', 'reembolsado');

-- Orders
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_number VARCHAR(50) NOT NULL UNIQUE,
    user_id UUID REFERENCES app_users(id),
    status order_status DEFAULT 'nuevo',
    
    -- Customer info
    customer_email VARCHAR(255) NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    customer_phone VARCHAR(20) NOT NULL,
    
    -- Shipping address
    shipping_address_line1 VARCHAR(255) NOT NULL,
    shipping_address_line2 VARCHAR(255),
    shipping_city VARCHAR(100) NOT NULL,
    shipping_state VARCHAR(100) NOT NULL,
    shipping_municipality VARCHAR(100),
    shipping_postal_code VARCHAR(20),
    shipping_country VARCHAR(2) DEFAULT 'GT',
    
    -- Billing address (optional, if different)
    billing_address_line1 VARCHAR(255),
    billing_address_line2 VARCHAR(255),
    billing_city VARCHAR(100),
    billing_state VARCHAR(100),
    billing_postal_code VARCHAR(20),
    billing_country VARCHAR(2) DEFAULT 'GT',
    
    -- Amounts
    subtotal DECIMAL(10, 2) NOT NULL,
    tax_amount DECIMAL(10, 2) DEFAULT 0,
    shipping_amount DECIMAL(10, 2) DEFAULT 0,
    discount_amount DECIMAL(10, 2) DEFAULT 0,
    total DECIMAL(10, 2) NOT NULL,
    
    -- Shipping
    shipping_method VARCHAR(100), -- 'delivery', 'pickup'
    shipping_notes TEXT,
    
    -- Payment
    payment_method VARCHAR(50), -- 'sandbox', 'card', 'transfer', etc.
    payment_status VARCHAR(50) DEFAULT 'pending',
    
    -- Coupon
    coupon_code VARCHAR(50),
    
    -- Notes
    customer_notes TEXT,
    admin_notes TEXT,
    
    -- Timestamps
    paid_at TIMESTAMP WITH TIME ZONE,
    shipped_at TIMESTAMP WITH TIME ZONE,
    delivered_at TIMESTAMP WITH TIME ZONE,
    cancelled_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Order items
CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES products(id),
    variant_id UUID REFERENCES product_variants(id),
    sku VARCHAR(100) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    variant_name VARCHAR(255),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL,
    tax_rate DECIMAL(5, 2) DEFAULT 0,
    subtotal DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- PAYMENTS
-- =====================================================

-- Payment status enum
CREATE TYPE payment_status AS ENUM ('pending', 'processing', 'completed', 'failed', 'refunded');

-- Payments
CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    payment_method VARCHAR(50) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'GTQ',
    status payment_status DEFAULT 'pending',
    transaction_id VARCHAR(255),
    gateway_response JSONB,
    error_message TEXT,
    processed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- SHIPPING
-- =====================================================

-- Shipping zones (departamentos de Guatemala)
CREATE TABLE shipping_zones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    type VARCHAR(50) DEFAULT 'department', -- 'department', 'municipality'
    parent_id UUID REFERENCES shipping_zones(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Shipping rates
CREATE TABLE shipping_rates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    zone_id UUID NOT NULL REFERENCES shipping_zones(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    rate DECIMAL(10, 2) NOT NULL,
    min_order_amount DECIMAL(10, 2) DEFAULT 0,
    free_shipping_threshold DECIMAL(10, 2),
    estimated_days_min INTEGER,
    estimated_days_max INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Shipments
CREATE TABLE shipments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    tracking_number VARCHAR(255),
    carrier VARCHAR(100),
    shipped_at TIMESTAMP WITH TIME ZONE,
    estimated_delivery TIMESTAMP WITH TIME ZONE,
    delivered_at TIMESTAMP WITH TIME ZONE,
    status VARCHAR(50) DEFAULT 'pending',
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- COUPONS & DISCOUNTS
-- =====================================================

-- Coupon type enum
CREATE TYPE coupon_type AS ENUM ('percentage', 'fixed_amount');

-- Coupons
CREATE TABLE coupons (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(50) NOT NULL UNIQUE,
    type coupon_type NOT NULL,
    value DECIMAL(10, 2) NOT NULL,
    min_purchase_amount DECIMAL(10, 2) DEFAULT 0,
    max_discount_amount DECIMAL(10, 2),
    usage_limit INTEGER,
    usage_count INTEGER DEFAULT 0,
    valid_from TIMESTAMP WITH TIME ZONE,
    valid_until TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Coupon usage tracking
CREATE TABLE coupon_usage (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coupon_id UUID NOT NULL REFERENCES coupons(id) ON DELETE CASCADE,
    order_id UUID NOT NULL REFERENCES orders(id),
    user_id UUID REFERENCES app_users(id),
    discount_amount DECIMAL(10, 2) NOT NULL,
    used_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- CONTENT MANAGEMENT
-- =====================================================

-- Banners
CREATE TABLE banners (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    subtitle TEXT,
    image_url TEXT NOT NULL,
    mobile_image_url TEXT,
    link_url TEXT,
    link_text VARCHAR(100),
    position VARCHAR(50) DEFAULT 'home-hero', -- 'home-hero', 'home-secondary', 'category'
    display_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    valid_from TIMESTAMP WITH TIME ZONE,
    valid_until TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Pages (contenido estático)
CREATE TABLE pages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    slug VARCHAR(255) NOT NULL UNIQUE,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    meta_title VARCHAR(255),
    meta_description TEXT,
    is_published BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- AUDIT & LOGS
-- =====================================================

-- Audit logs
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES app_users(id),
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100) NOT NULL,
    entity_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- INDEXES
-- =====================================================

-- Users
CREATE INDEX idx_app_users_email ON app_users(email);
CREATE INDEX idx_app_users_role ON app_users(role);
CREATE INDEX idx_addresses_user_id ON addresses(user_id);

-- Catalog
CREATE INDEX idx_brands_slug ON brands(slug);
CREATE INDEX idx_categories_parent_id ON categories(parent_id);
CREATE INDEX idx_categories_slug ON categories(slug);
CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_products_slug ON products(slug);
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_products_brand_id ON products(brand_id);
CREATE INDEX idx_products_status ON products(status);
CREATE INDEX idx_products_name_trgm ON products USING gin(name gin_trgm_ops);
CREATE INDEX idx_product_variants_product_id ON product_variants(product_id);
CREATE INDEX idx_product_variants_sku ON product_variants(sku);
CREATE INDEX idx_product_images_product_id ON product_images(product_id);

-- Shopping
CREATE INDEX idx_carts_user_id ON carts(user_id);
CREATE INDEX idx_carts_session_id ON carts(session_id);
CREATE INDEX idx_cart_items_cart_id ON cart_items(cart_id);
CREATE INDEX idx_wishlists_user_id ON wishlists(user_id);

-- Orders
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_order_number ON orders(order_number);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created_at ON orders(created_at DESC);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);

-- Payments
CREATE INDEX idx_payments_order_id ON payments(order_id);
CREATE INDEX idx_payments_status ON payments(status);

-- Shipments
CREATE INDEX idx_shipments_order_id ON shipments(order_id);

-- Coupons
CREATE INDEX idx_coupons_code ON coupons(code);
CREATE INDEX idx_coupon_usage_coupon_id ON coupon_usage(coupon_id);

-- Audit
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at DESC);

-- =====================================================
-- TRIGGERS
-- =====================================================

-- Update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to all tables with updated_at
CREATE TRIGGER update_app_users_updated_at BEFORE UPDATE ON app_users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_addresses_updated_at BEFORE UPDATE ON addresses FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_brands_updated_at BEFORE UPDATE ON brands FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_categories_updated_at BEFORE UPDATE ON categories FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_product_variants_updated_at BEFORE UPDATE ON product_variants FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_carts_updated_at BEFORE UPDATE ON carts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_cart_items_updated_at BEFORE UPDATE ON cart_items FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_orders_updated_at BEFORE UPDATE ON orders FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_payments_updated_at BEFORE UPDATE ON payments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_shipments_updated_at BEFORE UPDATE ON shipments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_coupons_updated_at BEFORE UPDATE ON coupons FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_banners_updated_at BEFORE UPDATE ON banners FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_pages_updated_at BEFORE UPDATE ON pages FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Enable pg_trgm for search
CREATE EXTENSION IF NOT EXISTS pg_trgm;
