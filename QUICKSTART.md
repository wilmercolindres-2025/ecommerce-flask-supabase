# 🚀 Quick Start Guide - La Bodegona

Guía rápida para poner en marcha La Bodegona en 15 minutos.

## ⚡ Setup Rápido (Local)

### 1. Clonar y Configurar

```bash
# Si estás trabajando desde GitHub web, descarga el repositorio
# O clona si ya está en GitHub:
git clone https://github.com/tu-usuario/ecommerce-flask-supabase.git
cd ecommerce-flask-supabase

# Copiar variables de entorno
cp .env.example .env
```

### 2. Configurar Supabase (5 minutos)

1. Ve a [supabase.com](https://supabase.com) → Crear proyecto
2. Copia las credenciales a `.env`:
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY`
   - `DATABASE_URL`

3. En Supabase SQL Editor, ejecuta en orden:
   ```
   supabase/migrations/00_schema.sql
   supabase/migrations/01_rls.sql
   supabase/migrations/02_seed.sql
   supabase/migrations/03_storage.sql
   ```

### 3. Instalar Dependencias (3 minutos)

```bash
# Python
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Node.js
npm install
```

### 4. Compilar Assets (1 minuto)

```bash
npm run build
```

### 5. Crear Usuario Admin (1 minuto)

```bash
python manage.py create-admin --email admin@labodegona.gt --password Admin#2025! --name Administrador
```

### 6. Ejecutar (1 minuto)

```bash
flask run
```

Abre http://localhost:5000 🎉

---

## 🌐 Despliegue a Producción (GitHub + Render)

### 1. Subir a GitHub (2 minutos)

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/tu-usuario/tu-repo.git
git push -u origin main
```

### 2. Configurar Secrets en GitHub (3 minutos)

Settings → Secrets and variables → Actions → New repository secret

Agregar:
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`
- `DATABASE_URL`
- `FLASK_SECRET_KEY` (genera con: `python -c "import secrets; print(secrets.token_hex(32))"`)
- `RENDER_API_KEY` (obtener de Render después)
- `RENDER_SERVICE_ID` (obtener de Render después)

### 3. Crear Servicio en Render (5 minutos)

1. Ve a [render.com](https://render.com) → New Web Service
2. Conecta tu repositorio de GitHub
3. Configuración:
   - **Build Command**: `pip install -r requirements.txt && npm install && npm run build`
   - **Start Command**: `gunicorn "app:create_app()" --bind 0.0.0.0:$PORT`
   - **Environment**: Agrega todas las variables de `.env`

4. Obtén API Key y Service ID:
   - Account Settings → API Keys → Create
   - Copia Service ID de la URL del servicio
   - Agrégalos como secrets en GitHub

### 4. Deploy Automático (5 minutos)

Cada push a `main` desplegará automáticamente vía GitHub Actions.

```bash
git push origin main
```

Espera 5-10 minutos y tu app estará en línea! 🚀

---

## 📋 Checklist Post-Despliegue

- [ ] Verificar que la app carga en la URL de Render
- [ ] Login con usuario admin funciona
- [ ] Panel `/admin` es accesible
- [ ] Productos se muestran correctamente
- [ ] Agregar al carrito funciona
- [ ] Proceso de checkout completo funciona
- [ ] Imágenes se cargan desde Supabase Storage
- [ ] WhatsApp link funciona

---

## 🆘 Problemas Comunes

### "Database connection failed"
→ Verifica `DATABASE_URL` en variables de entorno

### "Module not found"
→ Ejecuta `pip install -r requirements.txt`

### "Storage bucket not found"
→ Ejecuta `03_storage.sql` en Supabase

### Imágenes no cargan
→ Verifica políticas de Storage en Supabase (lectura pública)

---

## 📚 Próximos Pasos

1. **Personalizar branding**: Edita `tailwind.config.js` para cambiar colores
2. **Agregar productos**: Ve a `/admin/productos/nuevo`
3. **Configurar dominio**: En Render → Settings → Custom Domains
4. **Configurar pagos reales**: Integra pasarela de pagos (Stripe, etc.)
5. **Email transaccional**: Configura SMTP real para notificaciones

---

## 📖 Documentación Completa

- [README.md](README.md) - Documentación principal
- [DEPLOYMENT.md](DEPLOYMENT.md) - Guía de despliegue detallada
- [CONTRIBUTING.md](CONTRIBUTING.md) - Guía de contribución

---

¡Listo para vender! 🛒💰
