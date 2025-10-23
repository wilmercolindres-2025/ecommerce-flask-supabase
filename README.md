# 🛒 La Bodegona - E-Commerce Completo

E-commerce completo listo para producción con Python Flask, Supabase (PostgreSQL + Auth + Storage) y despliegue automatizado en Render con GitHub Actions.

**La Bodegona** es una plataforma de comercio electrónico moderna, escalable y lista para usar en Guatemala, con catálogo completo, gestión de inventario, dashboard administrativo integral y experiencia de usuario optimizada.

## 🎨 Paleta de Colores

- **Primario**: `#1C3FAA` (Azul profundo)
- **Acento**: `#FFB020` (Naranja dorado)
- **Éxito**: `#10B981` (Verde)
- **Error**: `#EF4444` (Rojo)
- **Neutros**: Escala de grises (`#F9FAFB` a `#111827`)

## 🚀 Características

### MVP Completo
- ✅ Catálogo con categorías, subcategorías, marcas y variaciones
- ✅ Búsqueda, filtros y ordenamientos
- ✅ Carrito persistente y wishlist
- ✅ Checkout completo (datos, envío, confirmación)
- ✅ Autenticación con Supabase Auth (email/password)
- ✅ Roles: Administrador, Gestor, Cliente
- ✅ Panel Admin completo (CRUD productos, pedidos, reportes)
- ✅ Pagos en modo sandbox (preparado para integración real)
- ✅ Envíos por departamento/municipio (Guatemala) + pickup
- ✅ Integración WhatsApp con mensaje prellenado
- ✅ Páginas institucionales (Nosotros, Contacto, Términos, etc.)
- ✅ Localización español (Guatemala), moneda GTQ (Q)

### Gestión de Productos (Solo Administrador)
- Alta/edición completa de productos
- Múltiples imágenes con Supabase Storage
- Variaciones (talla/color), SKU único
- Estados: borrador, pendiente, publicado, oculto
- Validaciones estrictas
- Historial de cambios (auditoría)
- Vista previa antes de publicar

## 📋 Requisitos Previos

- Python 3.12+
- Node.js 18+ (para TailwindCSS)
- Cuenta en [Supabase](https://supabase.com)
- Cuenta en [Render](https://render.com) o [Railway](https://railway.app)
- Git y GitHub

## 🛠️ Setup Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/ecommerce-flask-supabase.git
cd ecommerce-flask-supabase
```

### 2. Crear proyecto en Supabase

1. Ve a [supabase.com](https://supabase.com) y crea un nuevo proyecto
2. Anota las credenciales:
   - `SUPABASE_URL`: URL de tu proyecto
   - `SUPABASE_ANON_KEY`: Clave anónima (pública)
   - `SUPABASE_SERVICE_ROLE_KEY`: Clave de servicio (privada, solo server)
   - `DATABASE_URL`: Connection string de PostgreSQL

### 3. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita `.env` con tus credenciales:

```env
# Flask
FLASK_ENV=development
FLASK_SECRET_KEY=tu-clave-secreta-muy-segura
FLASK_DEBUG=True

# Supabase
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_ANON_KEY=tu-anon-key
SUPABASE_SERVICE_ROLE_KEY=tu-service-role-key
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.tu-proyecto.supabase.co:5432/postgres

# Email (simulado en desarrollo)
MAIL_SERVER=localhost
MAIL_PORT=1025
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_USE_TLS=False
MAIL_DEFAULT_SENDER=noreply@tutienda.com

# WhatsApp
WHATSAPP_PHONE=+50212345678

# Pagos (sandbox)
PAYMENT_MODE=sandbox
```

### 4. Instalar dependencias

```bash
# Python
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt

# Node.js (TailwindCSS)
npm install
```

### 5. Provisionar base de datos

Ejecuta las migraciones en Supabase:

```bash
# Opción 1: Usando el script de Python
python manage.py provision

# Opción 2: Manualmente en Supabase SQL Editor
# Ejecuta en orden los archivos de supabase/migrations/
```

Esto creará:
- ✅ Esquema completo de tablas
- ✅ Políticas RLS
- ✅ Datos de ejemplo (categorías, marcas, productos, usuarios)
- ✅ Bucket de Storage para imágenes

### 6. Crear usuario administrador

```bash
python manage.py create-admin --email admin@tutienda.com --password Admin123!
```

### 7. Compilar assets

```bash
npm run build
```

### 8. Ejecutar en desarrollo

```bash
# Opción 1: Usando Make
make dev

# Opción 2: Directamente
flask run

# Opción 3: Con hot-reload de Tailwind
npm run dev  # En una terminal
flask run    # En otra terminal
```

La aplicación estará disponible en `http://localhost:5000`

## 🧪 Tests

```bash
# Todos los tests
make test

# Solo unitarios
pytest tests/unit -v

# Solo integración
pytest tests/integration -v

# Con cobertura
pytest --cov=app --cov-report=html

# E2E con Playwright
pytest tests/e2e -v
```

## 📦 Comandos Make

```bash
make dev          # Ejecutar en desarrollo
make test         # Ejecutar tests
make seed         # Cargar datos de ejemplo
make deploy       # Desplegar (via GitHub Actions)
make lint         # Linter (flake8/ruff)
make format       # Formatear código (black)
make clean        # Limpiar archivos temporales
```

## 🚢 Despliegue

### Configuración en Render/Railway

#### Opción 1: Render

1. Conecta tu repositorio de GitHub
2. Crea un nuevo **Web Service**
3. Configura:
   - **Build Command**: `pip install -r requirements.txt && npm install && npm run build`
   - **Start Command**: `gunicorn "app:create_app()" --bind 0.0.0.0:$PORT`
4. Agrega las variables de entorno desde `.env.example`
5. Despliega

#### Opción 2: Railway

1. Conecta tu repositorio de GitHub
2. Crea un nuevo proyecto
3. Railway detectará automáticamente el `Procfile`
4. Agrega las variables de entorno
5. Despliega

### GitHub Actions (Automático)

El despliegue se ejecuta automáticamente en cada push a `main`:

1. **CI**: Lint → Tests → Build
2. **Provision DB**: Aplica migraciones (manual o automático)
3. **Deploy**: Despliega a Render/Railway

#### Configurar Secrets en GitHub

Ve a `Settings > Secrets and variables > Actions` y agrega:

```
SUPABASE_URL
SUPABASE_ANON_KEY
SUPABASE_SERVICE_ROLE_KEY
DATABASE_URL
FLASK_SECRET_KEY
RENDER_API_KEY (o RAILWAY_TOKEN)
RENDER_SERVICE_ID (o RAILWAY_PROJECT_ID)
```

## 📁 Estructura del Proyecto

```
ecommerce-flask-supabase/
├── app/
│   ├── blueprints/
│   │   ├── admin/          # Panel de administración
│   │   ├── auth/           # Autenticación
│   │   ├── cart/           # Carrito de compras
│   │   ├── catalog/        # Catálogo y productos
│   │   ├── checkout/       # Proceso de compra
│   │   ├── main/           # Páginas principales
│   │   └── user/           # Perfil de usuario
│   ├── services/
│   │   ├── supabase.py     # Cliente Supabase
│   │   ├── auth.py         # Servicio de autenticación
│   │   ├── products.py     # Servicio de productos
│   │   ├── cart.py         # Servicio de carrito
│   │   ├── orders.py       # Servicio de pedidos
│   │   └── storage.py      # Servicio de Storage
│   ├── models/             # Modelos SQLAlchemy
│   ├── forms/              # Formularios Flask-WTF
│   ├── templates/          # Templates Jinja2
│   ├── static/
│   │   ├── css/            # CSS compilado
│   │   ├── js/             # JavaScript + HTMX
│   │   └── images/         # Imágenes estáticas
│   ├── utils/              # Utilidades
│   └── __init__.py         # Factory de aplicación
├── supabase/
│   └── migrations/
│       ├── 00_schema.sql   # Esquema de base de datos
│       ├── 01_rls.sql      # Políticas RLS
│       ├── 02_seed.sql     # Datos de ejemplo
│       └── 03_storage.sql  # Configuración Storage
├── tests/
│   ├── unit/               # Tests unitarios
│   ├── integration/        # Tests de integración
│   └── e2e/                # Tests end-to-end
├── .github/
│   └── workflows/
│       ├── ci.yml          # CI/CD principal
│       ├── deploy.yml      # Despliegue
│       └── provision-db.yml # Provisión de DB
├── infra/
│   ├── Procfile            # Para Render/Railway
│   └── render.yaml         # Configuración Render
├── manage.py               # CLI de gestión
├── requirements.txt        # Dependencias Python
├── package.json            # Dependencias Node.js
├── tailwind.config.js      # Configuración Tailwind
├── postcss.config.js       # PostCSS
├── pytest.ini              # Configuración pytest
├── .env.example            # Ejemplo de variables
└── README.md
```

## 👥 Usuarios de Prueba

Después de ejecutar el seed, tendrás estos usuarios:

| Email | Password | Rol |
|-------|----------|-----|
| admin@labodegona.gt | Admin#2025! | Administrador |
| cliente@labodegona.gt | Cliente#2025! | Cliente |

## 🎯 Pasos de Despliegue Completo

### 1. Crear Proyecto en Supabase

1. Ve a [supabase.com](https://supabase.com) y crea un nuevo proyecto
2. Espera a que el proyecto esté listo (2-3 minutos)
3. Ve a **Settings > API** y copia:
   - `SUPABASE_URL`: Project URL
   - `SUPABASE_ANON_KEY`: anon/public key
   - `SUPABASE_SERVICE_ROLE_KEY`: service_role key (¡mantén en secreto!)
4. Ve a **Settings > Database** y copia:
   - `DATABASE_URL`: Connection string (URI format)

### 2. Configurar GitHub Secrets

1. Ve a tu repositorio en GitHub
2. **Settings > Secrets and variables > Actions > New repository secret**
3. Agrega los siguientes secrets:

```
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_ANON_KEY=tu-anon-key
SUPABASE_SERVICE_ROLE_KEY=tu-service-role-key
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.tu-proyecto.supabase.co:5432/postgres
FLASK_SECRET_KEY=genera-una-clave-segura-aleatoria
```

### 3. Ejecutar Workflow de Provisión de Base de Datos

1. Ve a **Actions** en tu repositorio
2. Selecciona el workflow **"Provision Database"**
3. Click en **"Run workflow"** > **"Run workflow"**
4. Espera a que termine (aplica migraciones + seed)
5. Verifica en Supabase SQL Editor que las tablas fueron creadas

### 4. Crear Servicio en Render

1. Ve a [render.com](https://render.com) y conecta tu cuenta de GitHub
2. Click en **"New +"** > **"Web Service"**
3. Selecciona tu repositorio
4. Configura:
   - **Name**: `la-bodegona` (o el que prefieras)
   - **Region**: Oregon (US West) o el más cercano
   - **Branch**: `main`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt && npm install && npm run build`
   - **Start Command**: `gunicorn "app:create_app()" --bind 0.0.0.0:$PORT --workers 2`
5. En **Environment Variables**, agrega todas las variables del `.env.example`:

```
FLASK_ENV=production
FLASK_SECRET_KEY=tu-clave-secreta
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_ANON_KEY=tu-anon-key
SUPABASE_SERVICE_ROLE_KEY=tu-service-role-key
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.tu-proyecto.supabase.co:5432/postgres
APP_NAME=La Bodegona
CURRENCY=GTQ
CURRENCY_SYMBOL=Q
LOCALE=es_GT
WHATSAPP_PHONE=+50212345678
PAYMENT_MODE=sandbox
```

6. Click en **"Create Web Service"**
7. Espera a que el deploy termine (5-10 minutos)

### 5. Crear Usuario Administrador en Supabase

1. Ve a tu proyecto en Supabase
2. **Authentication > Users > Invite user**
3. Email: `admin@labodegona.gt`
4. Envía la invitación y completa el registro
5. Ve a **SQL Editor** y ejecuta:

```sql
-- Asignar rol de administrador
UPDATE app_users 
SET role = 'admin' 
WHERE email = 'admin@labodegona.gt';
```

### 6. Verificar Funcionamiento

1. Abre la URL de tu servicio en Render (ej: `https://la-bodegona.onrender.com`)
2. Verifica que la tienda carga correctamente
3. Ve a `/admin` e inicia sesión con `admin@labodegona.gt`
4. Verifica el Dashboard:
   - ✅ Productos cargados (30+)
   - ✅ Categorías (6+)
   - ✅ Marcas (6)
   - ✅ Pedidos de ejemplo (10)
5. Prueba crear un producto:
   - Sube imágenes (deben guardarse en Supabase Storage)
   - Publica el producto
   - Verifica que aparece en la tienda pública
6. Prueba el flujo de compra:
   - Agrega productos al carrito
   - Procede al checkout
   - Completa el pedido
   - Verifica que el stock se descuenta
   - Verifica que el pedido aparece en el Dashboard

### 7. Configurar CI/CD Automático (Opcional)

Si quieres deploys automáticos en cada push:

1. Ve a Render Dashboard > tu servicio > Settings
2. Copia el **Deploy Hook URL**
3. En GitHub: Settings > Secrets > Agregar:
   - `RENDER_DEPLOY_HOOK_URL`: la URL copiada
4. Edita `.github/workflows/deploy.yml` y descomenta la sección de Render

Ahora cada push a `main` desplegará automáticamente.

## 📊 Catálogo Inicial (Seed)

El proyecto incluye datos precargados para empezar a usarlo inmediatamente:

- **30+ productos** con imágenes, variantes y stock
- **6 categorías principales**: Electrónica, Moda, Hogar, Deportes, Belleza, Alimentos
- **6 marcas**: Samsung, Nike, Sony, Adidas, Apple, LG
- **10 pedidos de ejemplo** con diferentes estados
- **3 cupones activos**: BIENVENIDA10, VERANO20, ENVIOGRATIS
- **2 banners** para la página de inicio
- **Usuarios demo**: Admin y Cliente

## 🔒 Seguridad

- ✅ Row Level Security (RLS) activado en todas las tablas
- ✅ Políticas de acceso por rol
- ✅ CSRF protection con Flask-WTF
- ✅ Rate limiting con Flask-Limiter
- ✅ Sanitización de inputs
- ✅ Secrets en variables de entorno
- ✅ HTTPS obligatorio en producción
- ✅ Validación de imágenes antes de subir
- ✅ Auditoría de acciones críticas

## 🔒 Seguridad

- ✅ RLS (Row Level Security) en todas las tablas
- ✅ Validación server-side y client-side
- ✅ CSRF protection en formularios
- ✅ Rate limiting en endpoints críticos
- ✅ Sanitización de inputs
- ✅ Service Role Key solo en servidor
- ✅ Políticas de contraseñas fuertes
- ✅ Bloqueo tras intentos fallidos

## 📊 Reportes y Analytics

El panel de administración incluye:
- Ventas por rango de fechas
- Top productos más vendidos
- Top categorías
- Gráficos de tendencias
- Inventario bajo stock
- Pedidos por estado

## 🎨 Personalización de Branding

### Cambiar colores

Edita `tailwind.config.js`:

```js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#1C3FAA',    // Tu color primario
        accent: '#FFB020',     // Tu color de acento
        // ...
      }
    }
  }
}
```

Luego recompila:

```bash
npm run build
```

### Cambiar logo

Reemplaza los archivos en `app/static/images/`:
- `logo.svg` - Logo principal
- `logo-white.svg` - Logo para fondos oscuros
- `favicon.ico` - Favicon

## 📮 Colección Postman

Importa `postman_collection.json` en Postman para probar todos los endpoints.

## 🐛 Troubleshooting

### Error de conexión a Supabase

Verifica que `SUPABASE_URL` y las keys sean correctas. Prueba la conexión:

```bash
python manage.py test-connection
```

### Imágenes no se cargan

Verifica las políticas del bucket `products` en Supabase Storage:
- Lectura pública habilitada
- Subida solo para usuarios autenticados con rol Admin

### Migraciones fallan

Ejecuta las migraciones manualmente desde el SQL Editor de Supabase en orden:
1. `00_schema.sql`
2. `01_rls.sql`
3. `02_seed.sql`
4. `03_storage.sql`

## 📝 Licencia

MIT License - Ver `LICENSE` para más detalles.

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📧 Soporte

Para preguntas o soporte, abre un issue en GitHub.

---

**Desarrollado con ❤️ en Guatemala 🇬🇹**
