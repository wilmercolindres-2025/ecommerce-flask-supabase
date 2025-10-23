# Guía de Despliegue

Esta guía te ayudará a desplegar el e-commerce en producción usando Supabase y Render.

## Pre-requisitos

- Cuenta en [Supabase](https://supabase.com)
- Cuenta en [Render](https://render.com) o [Railway](https://railway.app)
- Cuenta en [GitHub](https://github.com)
- Git instalado localmente

## Paso 1: Configurar Supabase

### 1.1 Crear Proyecto

1. Ve a [supabase.com](https://supabase.com) y crea una cuenta
2. Crea un nuevo proyecto
3. Anota las credenciales:
   - **Project URL**: `https://tu-proyecto.supabase.co`
   - **Anon/Public Key**: Clave pública para el cliente
   - **Service Role Key**: Clave privada para operaciones del servidor

### 1.2 Obtener Connection String

1. En el dashboard de Supabase, ve a **Settings > Database**
2. Copia el **Connection String** en modo `URI`
3. Reemplaza `[YOUR-PASSWORD]` con tu contraseña de base de datos

Ejemplo:
```
postgresql://postgres:[PASSWORD]@db.tu-proyecto.supabase.co:5432/postgres
```

### 1.3 Ejecutar Migraciones

Opción A: Desde el SQL Editor de Supabase

1. Ve a **SQL Editor** en el dashboard
2. Ejecuta los archivos en orden:
   - `supabase/migrations/00_schema.sql`
   - `supabase/migrations/01_rls.sql`
   - `supabase/migrations/02_seed.sql`
   - `supabase/migrations/03_storage.sql`

Opción B: Usando GitHub Actions

1. Ve a tu repositorio en GitHub
2. **Actions > Provision Database > Run workflow**
3. Marca "Run seed data" si quieres datos de ejemplo
4. Ejecuta el workflow

### 1.4 Verificar Storage

1. Ve a **Storage** en el dashboard de Supabase
2. Verifica que existan los buckets:
   - `products`
   - `avatars`
   - `banners`
3. Verifica las políticas de acceso en cada bucket

## Paso 2: Configurar GitHub

### 2.1 Crear Repositorio

```bash
cd ecommerce-flask-supabase
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/tu-usuario/tu-repo.git
git push -u origin main
```

### 2.2 Configurar Secrets

Ve a **Settings > Secrets and variables > Actions** y agrega:

```
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_ANON_KEY=tu-anon-key
SUPABASE_SERVICE_ROLE_KEY=tu-service-role-key
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.tu-proyecto.supabase.co:5432/postgres
FLASK_SECRET_KEY=genera-una-clave-secreta-segura
RENDER_API_KEY=tu-render-api-key
RENDER_SERVICE_ID=tu-render-service-id
```

Para generar `FLASK_SECRET_KEY`:
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

## Paso 3: Desplegar en Render

### 3.1 Crear Servicio

1. Ve a [render.com](https://render.com) y crea una cuenta
2. Conecta tu cuenta de GitHub
3. Crea un nuevo **Web Service**
4. Selecciona tu repositorio

### 3.2 Configurar Servicio

**Build Command:**
```bash
pip install -r requirements.txt && npm install && npm run build
```

**Start Command:**
```bash
gunicorn "app:create_app()" --bind 0.0.0.0:$PORT
```

**Environment Variables:**

```
PYTHON_VERSION=3.12.0
FLASK_ENV=production
FLASK_SECRET_KEY=[tu-clave-secreta]
SUPABASE_URL=[tu-supabase-url]
SUPABASE_ANON_KEY=[tu-anon-key]
SUPABASE_SERVICE_ROLE_KEY=[tu-service-role-key]
DATABASE_URL=[tu-database-url]
APP_NAME=Mi Tienda GT
CURRENCY=GTQ
CURRENCY_SYMBOL=Q
LOCALE=es_GT
WHATSAPP_PHONE=+50212345678
PAYMENT_MODE=sandbox
```

### 3.3 Obtener API Key de Render

1. Ve a **Account Settings > API Keys**
2. Crea una nueva API Key
3. Copia el **Service ID** de tu servicio (está en la URL)
4. Agrega ambos como secrets en GitHub

## Paso 4: Crear Usuario Administrador

### Opción A: Desde Supabase Dashboard

1. Ve a **Authentication > Users**
2. Crea un nuevo usuario con email y password
3. Copia el **User ID**
4. Ve a **SQL Editor** y ejecuta:

```sql
INSERT INTO app_users (id, email, full_name, role, email_verified)
VALUES ('user-id-copiado', 'admin@tutienda.com', 'Administrador', 'admin', true);
```

### Opción B: Usando CLI (localmente)

```bash
python manage.py create-admin --email admin@tutienda.com --password Admin123! --name Administrador
```

## Paso 5: Verificar Despliegue

1. Espera a que el despliegue termine (5-10 minutos)
2. Visita la URL de tu aplicación en Render
3. Verifica que la página de inicio cargue correctamente
4. Inicia sesión con el usuario administrador
5. Ve a `/admin` y verifica el panel de administración

## Paso 6: Configurar Dominio Personalizado (Opcional)

### En Render:

1. Ve a **Settings > Custom Domains**
2. Agrega tu dominio
3. Configura los registros DNS según las instrucciones
4. Espera a que se active el certificado SSL

## Paso 7: Configurar CI/CD

El CI/CD ya está configurado con GitHub Actions. Cada push a `main` disparará:

1. **Lint**: Verifica el código
2. **Tests**: Ejecuta las pruebas
3. **Build**: Compila los assets
4. **Deploy**: Despliega a Render automáticamente

## Troubleshooting

### Error: "Database connection failed"

- Verifica que `DATABASE_URL` esté correctamente configurado
- Asegúrate de que la contraseña no tenga caracteres especiales sin escapar
- Verifica que el proyecto de Supabase esté activo

### Error: "Module not found"

- Verifica que `requirements.txt` esté completo
- Asegúrate de que el build command incluya `pip install -r requirements.txt`

### Error: "Storage bucket not found"

- Ejecuta `03_storage.sql` en el SQL Editor de Supabase
- Verifica que los buckets existan en **Storage**

### Las imágenes no se cargan

- Verifica las políticas de Storage en Supabase
- Asegúrate de que el bucket `products` tenga lectura pública habilitada

### El admin no puede subir imágenes

- Verifica que el usuario tenga rol `admin` en la tabla `app_users`
- Verifica las políticas de escritura en el bucket `products`

## Monitoreo

### Logs en Render

1. Ve a tu servicio en Render
2. Click en **Logs** para ver los logs en tiempo real

### Métricas en Supabase

1. Ve a **Reports** en el dashboard de Supabase
2. Monitorea el uso de la base de datos y storage

## Backup

### Base de Datos

Supabase hace backups automáticos diarios. Para backup manual:

1. Ve a **Database > Backups**
2. Click en **Create Backup**

### Storage

Descarga los archivos importantes del Storage:

```bash
# Usando Supabase CLI
supabase storage download products --recursive
```

## Actualizaciones

Para actualizar la aplicación:

1. Haz cambios en tu código local
2. Commit y push a GitHub:
   ```bash
   git add .
   git commit -m "Descripción de cambios"
   git push origin main
   ```
3. GitHub Actions desplegará automáticamente

## Rollback

Si necesitas revertir a una versión anterior:

1. En Render, ve a **Deploys**
2. Encuentra el deploy anterior exitoso
3. Click en **Redeploy**

## Soporte

Si tienes problemas:

1. Revisa los logs en Render
2. Verifica las variables de entorno
3. Consulta la documentación de Supabase
4. Abre un issue en GitHub

---

¡Felicidades! Tu e-commerce está en producción 🎉
