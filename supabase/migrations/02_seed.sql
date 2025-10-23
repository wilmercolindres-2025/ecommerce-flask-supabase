-- =====================================================
-- Seed Data for E-Commerce
-- =====================================================

-- =====================================================
-- APP ROLES
-- =====================================================

INSERT INTO app_roles (name, description) VALUES
('admin', 'Administrador con acceso completo al sistema'),
('gestor', 'Gestor de contenido con permisos limitados'),
('cliente', 'Cliente regular de la tienda');

-- =====================================================
-- SHIPPING ZONES (Departamentos de Guatemala)
-- =====================================================

INSERT INTO shipping_zones (id, name, type) VALUES
('d1000000-0000-0000-0000-000000000001', 'Guatemala', 'department'),
('d1000000-0000-0000-0000-000000000002', 'Alta Verapaz', 'department'),
('d1000000-0000-0000-0000-000000000003', 'Baja Verapaz', 'department'),
('d1000000-0000-0000-0000-000000000004', 'Chimaltenango', 'department'),
('d1000000-0000-0000-0000-000000000005', 'Chiquimula', 'department'),
('d1000000-0000-0000-0000-000000000006', 'El Progreso', 'department'),
('d1000000-0000-0000-0000-000000000007', 'Escuintla', 'department'),
('d1000000-0000-0000-0000-000000000008', 'Huehuetenango', 'department'),
('d1000000-0000-0000-0000-000000000009', 'Izabal', 'department'),
('d1000000-0000-0000-0000-000000000010', 'Jalapa', 'department'),
('d1000000-0000-0000-0000-000000000011', 'Jutiapa', 'department'),
('d1000000-0000-0000-0000-000000000012', 'Petén', 'department'),
('d1000000-0000-0000-0000-000000000013', 'Quetzaltenango', 'department'),
('d1000000-0000-0000-0000-000000000014', 'Quiché', 'department'),
('d1000000-0000-0000-0000-000000000015', 'Retalhuleu', 'department'),
('d1000000-0000-0000-0000-000000000016', 'Sacatepéquez', 'department'),
('d1000000-0000-0000-0000-000000000017', 'San Marcos', 'department'),
('d1000000-0000-0000-0000-000000000018', 'Santa Rosa', 'department'),
('d1000000-0000-0000-0000-000000000019', 'Sololá', 'department'),
('d1000000-0000-0000-0000-000000000020', 'Suchitepéquez', 'department'),
('d1000000-0000-0000-0000-000000000021', 'Totonicapán', 'department'),
('d1000000-0000-0000-0000-000000000022', 'Zacapa', 'department');

-- =====================================================
-- SHIPPING RATES
-- =====================================================

-- Guatemala (capital) - envío más económico
INSERT INTO shipping_rates (zone_id, name, description, rate, free_shipping_threshold, estimated_days_min, estimated_days_max) VALUES
('d1000000-0000-0000-0000-000000000001', 'Envío Estándar', 'Entrega en 1-2 días hábiles', 25.00, 500.00, 1, 2);

-- Departamentos cercanos
INSERT INTO shipping_rates (zone_id, name, description, rate, free_shipping_threshold, estimated_days_min, estimated_days_max) VALUES
('d1000000-0000-0000-0000-000000000004', 'Envío Estándar', 'Entrega en 2-3 días hábiles', 35.00, 600.00, 2, 3),
('d1000000-0000-0000-0000-000000000007', 'Envío Estándar', 'Entrega en 2-3 días hábiles', 35.00, 600.00, 2, 3),
('d1000000-0000-0000-0000-000000000016', 'Envío Estándar', 'Entrega en 1-2 días hábiles', 30.00, 550.00, 1, 2);

-- Departamentos lejanos
INSERT INTO shipping_rates (zone_id, name, description, rate, free_shipping_threshold, estimated_days_min, estimated_days_max) VALUES
('d1000000-0000-0000-0000-000000000002', 'Envío Estándar', 'Entrega en 3-5 días hábiles', 50.00, 700.00, 3, 5),
('d1000000-0000-0000-0000-000000000008', 'Envío Estándar', 'Entrega en 3-5 días hábiles', 55.00, 750.00, 3, 5),
('d1000000-0000-0000-0000-000000000012', 'Envío Estándar', 'Entrega en 4-6 días hábiles', 65.00, 800.00, 4, 6),
('d1000000-0000-0000-0000-000000000013', 'Envío Estándar', 'Entrega en 3-4 días hábiles', 45.00, 700.00, 3, 4);

-- =====================================================
-- BRANDS
-- =====================================================

INSERT INTO brands (id, name, slug, description) VALUES
('b1000000-0000-0000-0000-000000000001', 'TechPro', 'techpro', 'Tecnología profesional de alta calidad'),
('b1000000-0000-0000-0000-000000000002', 'StyleWear', 'stylewear', 'Moda contemporánea y elegante'),
('b1000000-0000-0000-0000-000000000003', 'HomeComfort', 'homecomfort', 'Productos para el hogar y confort'),
('b1000000-0000-0000-0000-000000000004', 'SportMax', 'sportmax', 'Equipamiento deportivo de alto rendimiento'),
('b1000000-0000-0000-0000-000000000005', 'BeautyEssence', 'beautyessence', 'Belleza y cuidado personal'),
('b1000000-0000-0000-0000-000000000006', 'KidsWorld', 'kidsworld', 'Productos para niños y bebés'),
('b1000000-0000-0000-0000-000000000007', 'GourmetPlus', 'gourmetplus', 'Alimentos gourmet y especialidades');

-- =====================================================
-- CATEGORIES
-- =====================================================

-- Categorías principales
INSERT INTO categories (id, parent_id, name, slug, description, icon, display_order) VALUES
('c1000000-0000-0000-0000-000000000001', NULL, 'Electrónica', 'electronica', 'Dispositivos y accesorios electrónicos', 'laptop', 1),
('c1000000-0000-0000-0000-000000000002', NULL, 'Moda', 'moda', 'Ropa y accesorios de moda', 'shirt', 2),
('c1000000-0000-0000-0000-000000000003', NULL, 'Hogar', 'hogar', 'Productos para el hogar', 'home', 3),
('c1000000-0000-0000-0000-000000000004', NULL, 'Deportes', 'deportes', 'Equipamiento deportivo', 'dumbbell', 4),
('c1000000-0000-0000-0000-000000000005', NULL, 'Belleza', 'belleza', 'Productos de belleza y cuidado personal', 'sparkles', 5),
('c1000000-0000-0000-0000-000000000006', NULL, 'Juguetes', 'juguetes', 'Juguetes y entretenimiento', 'gamepad-2', 6),
('c1000000-0000-0000-0000-000000000007', NULL, 'Alimentos', 'alimentos', 'Alimentos y bebidas', 'utensils', 7);

-- Subcategorías de Electrónica
INSERT INTO categories (id, parent_id, name, slug, description, display_order) VALUES
('c1000000-0000-0000-0000-000000000101', 'c1000000-0000-0000-0000-000000000001', 'Computadoras', 'computadoras', 'Laptops, desktops y accesorios', 1),
('c1000000-0000-0000-0000-000000000102', 'c1000000-0000-0000-0000-000000000001', 'Smartphones', 'smartphones', 'Teléfonos inteligentes', 2),
('c1000000-0000-0000-0000-000000000103', 'c1000000-0000-0000-0000-000000000001', 'Audio', 'audio', 'Audífonos, bocinas y equipos de audio', 3),
('c1000000-0000-0000-0000-000000000104', 'c1000000-0000-0000-0000-000000000001', 'Accesorios', 'accesorios-electronica', 'Cables, cargadores y más', 4);

-- Subcategorías de Moda
INSERT INTO categories (id, parent_id, name, slug, description, display_order) VALUES
('c1000000-0000-0000-0000-000000000201', 'c1000000-0000-0000-0000-000000000002', 'Ropa Hombre', 'ropa-hombre', 'Ropa para caballero', 1),
('c1000000-0000-0000-0000-000000000202', 'c1000000-0000-0000-0000-000000000002', 'Ropa Mujer', 'ropa-mujer', 'Ropa para dama', 2),
('c1000000-0000-0000-0000-000000000203', 'c1000000-0000-0000-0000-000000000002', 'Calzado', 'calzado', 'Zapatos y zapatillas', 3),
('c1000000-0000-0000-0000-000000000204', 'c1000000-0000-0000-0000-000000000002', 'Accesorios', 'accesorios-moda', 'Bolsos, cinturones y más', 4);

-- Subcategorías de Hogar
INSERT INTO categories (id, parent_id, name, slug, description, display_order) VALUES
('c1000000-0000-0000-0000-000000000301', 'c1000000-0000-0000-0000-000000000003', 'Muebles', 'muebles', 'Muebles para el hogar', 1),
('c1000000-0000-0000-0000-000000000302', 'c1000000-0000-0000-0000-000000000003', 'Decoración', 'decoracion', 'Artículos decorativos', 2),
('c1000000-0000-0000-0000-000000000303', 'c1000000-0000-0000-0000-000000000003', 'Cocina', 'cocina', 'Utensilios y electrodomésticos', 3);

-- =====================================================
-- PRODUCTS
-- =====================================================

-- Productos de Electrónica
INSERT INTO products (id, sku, name, slug, short_description, description, technical_specs, category_id, brand_id, base_price, sale_price, status, is_featured) VALUES
('p1000000-0000-0000-0000-000000000001', 'LAPTOP-TP-001', 'Laptop TechPro X1', 'laptop-techpro-x1', 
'Laptop profesional de alto rendimiento', 
'Laptop TechPro X1 con procesador Intel Core i7, 16GB RAM, SSD 512GB. Ideal para trabajo profesional y gaming ligero.',
'{"processor": "Intel Core i7-12700H", "ram": "16GB DDR4", "storage": "512GB NVMe SSD", "display": "15.6\" Full HD IPS", "graphics": "Intel Iris Xe", "battery": "8 horas", "weight": "1.8kg"}',
'c1000000-0000-0000-0000-000000000101', 'b1000000-0000-0000-0000-000000000001', 8999.00, 7999.00, 'publicado', true),

('p1000000-0000-0000-0000-000000000002', 'PHONE-TP-001', 'Smartphone TechPro S20', 'smartphone-techpro-s20',
'Smartphone 5G de última generación',
'TechPro S20 con pantalla AMOLED de 6.5", cámara triple de 108MP, batería de 5000mAh y carga rápida de 65W.',
'{"display": "6.5\" AMOLED 120Hz", "processor": "Snapdragon 8 Gen 2", "ram": "8GB", "storage": "256GB", "camera": "108MP + 12MP + 5MP", "battery": "5000mAh", "5g": true}',
'c1000000-0000-0000-0000-000000000102', 'b1000000-0000-0000-0000-000000000001', 5499.00, 4999.00, 'publicado', true),

('p1000000-0000-0000-0000-000000000003', 'AUDIO-TP-001', 'Audífonos TechPro Wireless Pro', 'audifonos-techpro-wireless-pro',
'Audífonos inalámbricos con cancelación de ruido',
'Audífonos premium con cancelación activa de ruido, 30 horas de batería y sonido Hi-Fi.',
'{"type": "Over-ear", "connectivity": "Bluetooth 5.3", "anc": true, "battery": "30 horas", "driver": "40mm", "frequency": "20Hz-20kHz"}',
'c1000000-0000-0000-0000-000000000103', 'b1000000-0000-0000-0000-000000000001', 899.00, 749.00, 'publicado', true);

-- Productos de Moda
INSERT INTO products (id, sku, name, slug, short_description, description, category_id, brand_id, base_price, status, is_featured) VALUES
('p1000000-0000-0000-0000-000000000004', 'CAMISA-SW-001', 'Camisa StyleWear Casual', 'camisa-stylewear-casual',
'Camisa casual de algodón premium',
'Camisa de corte moderno en algodón 100%, perfecta para uso diario. Disponible en varios colores.',
'c1000000-0000-0000-0000-000000000201', 'b1000000-0000-0000-0000-000000000002', 299.00, 'publicado', false),

('p1000000-0000-0000-0000-000000000005', 'VESTIDO-SW-001', 'Vestido StyleWear Elegante', 'vestido-stylewear-elegante',
'Vestido elegante para ocasiones especiales',
'Vestido de corte A-line en tela de alta calidad, ideal para eventos formales.',
'c1000000-0000-0000-0000-000000000202', 'b1000000-0000-0000-0000-000000000002', 599.00, 'publicado', true),

('p1000000-0000-0000-0000-000000000006', 'ZAPATOS-SW-001', 'Zapatos StyleWear Sport', 'zapatos-stylewear-sport',
'Zapatos deportivos cómodos y modernos',
'Zapatillas deportivas con tecnología de amortiguación y diseño contemporáneo.',
'c1000000-0000-0000-0000-000000000203', 'b1000000-0000-0000-0000-000000000002', 449.00, 'publicado', false);

-- Productos de Hogar
INSERT INTO products (id, sku, name, slug, short_description, description, category_id, brand_id, base_price, sale_price, status) VALUES
('p1000000-0000-0000-0000-000000000007', 'SOFA-HC-001', 'Sofá HomeComfort Deluxe', 'sofa-homecomfort-deluxe',
'Sofá de 3 plazas ultra cómodo',
'Sofá tapizado en tela de alta resistencia con estructura de madera sólida. Incluye cojines decorativos.',
'c1000000-0000-0000-0000-000000000301', 'b1000000-0000-0000-0000-000000000003', 4999.00, 4499.00, 'publicado'),

('p1000000-0000-0000-0000-000000000008', 'LAMPARA-HC-001', 'Lámpara HomeComfort Modern', 'lampara-homecomfort-modern',
'Lámpara de pie estilo moderno',
'Lámpara de diseño minimalista con luz LED regulable y control remoto.',
'c1000000-0000-0000-0000-000000000302', 'b1000000-0000-0000-0000-000000000003', 799.00, NULL, 'publicado'),

('p1000000-0000-0000-0000-000000000009', 'LICUADORA-HC-001', 'Licuadora HomeComfort Power', 'licuadora-homecomfort-power',
'Licuadora de alta potencia',
'Licuadora de 1200W con jarra de vidrio de 2 litros y 5 velocidades.',
'c1000000-0000-0000-0000-000000000303', 'b1000000-0000-0000-0000-000000000003', 599.00, 499.00, 'publicado');

-- Productos de Deportes
INSERT INTO products (id, sku, name, slug, short_description, description, category_id, brand_id, base_price, status, is_featured) VALUES
('p1000000-0000-0000-0000-000000000010', 'BICI-SM-001', 'Bicicleta SportMax Mountain', 'bicicleta-sportmax-mountain',
'Bicicleta de montaña profesional',
'Bicicleta MTB con cuadro de aluminio, suspensión delantera y 21 velocidades.',
'c1000000-0000-0000-0000-000000000004', 'b1000000-0000-0000-0000-000000000004', 3499.00, 'publicado', true);

-- =====================================================
-- PRODUCT VARIANTS
-- =====================================================

-- Variantes para Camisa (tallas y colores)
INSERT INTO product_variants (product_id, sku, name, attributes, stock) VALUES
('p1000000-0000-0000-0000-000000000004', 'CAMISA-SW-001-S-AZUL', 'Talla S / Azul', '{"size": "S", "color": "Azul"}', 15),
('p1000000-0000-0000-0000-000000000004', 'CAMISA-SW-001-M-AZUL', 'Talla M / Azul', '{"size": "M", "color": "Azul"}', 25),
('p1000000-0000-0000-0000-000000000004', 'CAMISA-SW-001-L-AZUL', 'Talla L / Azul', '{"size": "L", "color": "Azul"}', 20),
('p1000000-0000-0000-0000-000000000004', 'CAMISA-SW-001-S-BLANCO', 'Talla S / Blanco', '{"size": "S", "color": "Blanco"}', 18),
('p1000000-0000-0000-0000-000000000004', 'CAMISA-SW-001-M-BLANCO', 'Talla M / Blanco', '{"size": "M", "color": "Blanco"}', 30),
('p1000000-0000-0000-0000-000000000004', 'CAMISA-SW-001-L-BLANCO', 'Talla L / Blanco', '{"size": "L", "color": "Blanco"}', 22);

-- Variantes para Vestido (tallas)
INSERT INTO product_variants (product_id, sku, name, attributes, stock) VALUES
('p1000000-0000-0000-0000-000000000005', 'VESTIDO-SW-001-S', 'Talla S', '{"size": "S"}', 10),
('p1000000-0000-0000-0000-000000000005', 'VESTIDO-SW-001-M', 'Talla M', '{"size": "M"}', 15),
('p1000000-0000-0000-0000-000000000005', 'VESTIDO-SW-001-L', 'Talla L', '{"size": "L"}', 12);

-- Variantes para Zapatos (tallas)
INSERT INTO product_variants (product_id, sku, name, attributes, stock) VALUES
('p1000000-0000-0000-0000-000000000006', 'ZAPATOS-SW-001-38', 'Talla 38', '{"size": "38"}', 8),
('p1000000-0000-0000-0000-000000000006', 'ZAPATOS-SW-001-39', 'Talla 39', '{"size": "39"}', 12),
('p1000000-0000-0000-0000-000000000006', 'ZAPATOS-SW-001-40', 'Talla 40', '{"size": "40"}', 15),
('p1000000-0000-0000-0000-000000000006', 'ZAPATOS-SW-001-41', 'Talla 41', '{"size": "41"}', 10),
('p1000000-0000-0000-0000-000000000006', 'ZAPATOS-SW-001-42', 'Talla 42', '{"size": "42"}', 8);

-- Stock para productos sin variantes
INSERT INTO product_variants (product_id, sku, name, attributes, stock) VALUES
('p1000000-0000-0000-0000-000000000001', 'LAPTOP-TP-001-STD', 'Estándar', '{}', 25),
('p1000000-0000-0000-0000-000000000002', 'PHONE-TP-001-STD', 'Estándar', '{}', 50),
('p1000000-0000-0000-0000-000000000003', 'AUDIO-TP-001-STD', 'Estándar', '{}', 40),
('p1000000-0000-0000-0000-000000000007', 'SOFA-HC-001-STD', 'Estándar', '{}', 8),
('p1000000-0000-0000-0000-000000000008', 'LAMPARA-HC-001-STD', 'Estándar', '{}', 15),
('p1000000-0000-0000-0000-000000000009', 'LICUADORA-HC-001-STD', 'Estándar', '{}', 30),
('p1000000-0000-0000-0000-000000000010', 'BICI-SM-001-STD', 'Estándar', '{}', 12);

-- =====================================================
-- COUPONS
-- =====================================================

INSERT INTO coupons (code, type, value, min_purchase_amount, usage_limit, valid_from, valid_until) VALUES
('BIENVENIDO10', 'percentage', 10.00, 200.00, 100, NOW(), NOW() + INTERVAL '30 days'),
('PRIMERACOMPRA', 'fixed_amount', 50.00, 500.00, 50, NOW(), NOW() + INTERVAL '60 days'),
('VERANO2024', 'percentage', 15.00, 300.00, 200, NOW(), NOW() + INTERVAL '90 days');

-- =====================================================
-- BANNERS
-- =====================================================

INSERT INTO banners (title, subtitle, image_url, link_url, link_text, position, display_order, valid_from, valid_until) VALUES
('Gran Venta de Tecnología', 'Hasta 30% de descuento en laptops y smartphones', '/static/images/banners/tech-sale.jpg', '/catalogo/electronica', 'Ver Ofertas', 'home-hero', 1, NOW(), NOW() + INTERVAL '30 days'),
('Nueva Colección de Moda', 'Descubre las últimas tendencias', '/static/images/banners/fashion-new.jpg', '/catalogo/moda', 'Explorar', 'home-hero', 2, NOW(), NOW() + INTERVAL '60 days'),
('Renueva tu Hogar', 'Muebles y decoración con envío gratis', '/static/images/banners/home-promo.jpg', '/catalogo/hogar', 'Comprar Ahora', 'home-secondary', 1, NOW(), NOW() + INTERVAL '45 days');

-- =====================================================
-- PAGES
-- =====================================================

INSERT INTO pages (slug, title, content, meta_title, meta_description, is_published) VALUES
('nosotros', 'Sobre Nosotros', 
'<h1>Nuestra Historia</h1><p>Somos una tienda guatemalteca comprometida con ofrecer productos de calidad a los mejores precios...</p>',
'Sobre Nosotros - Mi Tienda GT', 'Conoce nuestra historia y compromiso con Guatemala', true),

('contacto', 'Contacto', 
'<h1>Contáctanos</h1><p>Estamos aquí para ayudarte. Puedes comunicarte con nosotros por los siguientes medios...</p>',
'Contacto - Mi Tienda GT', 'Ponte en contacto con nuestro equipo', true),

('terminos', 'Términos y Condiciones', 
'<h1>Términos y Condiciones</h1><p>Al utilizar nuestro sitio web, aceptas los siguientes términos...</p>',
'Términos y Condiciones - Mi Tienda GT', 'Lee nuestros términos y condiciones', true),

('privacidad', 'Política de Privacidad', 
'<h1>Política de Privacidad</h1><p>Respetamos tu privacidad y protegemos tus datos personales...</p>',
'Política de Privacidad - Mi Tienda GT', 'Conoce cómo protegemos tu información', true),

('devoluciones', 'Política de Devoluciones', 
'<h1>Devoluciones y Cambios</h1><p>Tienes 30 días para devolver o cambiar tu producto...</p>',
'Política de Devoluciones - Mi Tienda GT', 'Información sobre devoluciones y cambios', true);

-- =====================================================
-- NOTA: Los usuarios se crean mediante Supabase Auth
-- Ejecutar después de crear el proyecto:
-- 1. Crear usuario admin mediante Supabase Dashboard o CLI
-- 2. Insertar en app_users con rol 'admin'
-- 3. Crear usuarios de prueba (gestor, cliente)
-- =====================================================

-- Ejemplo de cómo insertar usuarios después de crearlos en Supabase Auth:
-- INSERT INTO app_users (id, email, full_name, role) VALUES
-- ('[UUID del usuario de Supabase Auth]', 'admin@tutienda.com', 'Administrador', 'admin');
