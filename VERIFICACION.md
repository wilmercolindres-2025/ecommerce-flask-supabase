# ✅ Lista de Verificación - La Bodegona

Documento para verificar que todos los componentes del e-commerce están funcionando correctamente.

## 📋 Checklist de Funcionalidades

### 🏪 Tienda Pública

#### Página de Inicio
- [ ] Banners se muestran correctamente
- [ ] Productos destacados aparecen
- [ ] Categorías principales visibles
- [ ] Navegación funciona
- [ ] Búsqueda responde
- [ ] Carrito muestra contador

#### Catálogo
- [ ] Listado de productos carga
- [ ] Filtros por categoría funcionan
- [ ] Filtros por marca funcionan
- [ ] Filtro por rango de precio funciona
- [ ] Ordenamiento funciona (precio, nombre, novedades)
- [ ] Paginación funciona
- [ ] Imágenes cargan desde Supabase Storage

#### Detalle de Producto
- [ ] Información completa se muestra
- [ ] Galería de imágenes funciona
- [ ] Selector de variantes funciona
- [ ] Cantidad se puede ajustar
- [ ] Agregar al carrito funciona
- [ ] Stock se muestra correctamente
- [ ] Botón WhatsApp funciona
- [ ] Productos relacionados aparecen

#### Carrito
- [ ] Productos agregados aparecen
- [ ] Cantidad se puede modificar
- [ ] Eliminar producto funciona
- [ ] Subtotal calcula correctamente
- [ ] Cupón se puede aplicar
- [ ] Botón WhatsApp con resumen funciona
- [ ] Proceder a checkout funciona

#### Checkout
- [ ] Formulario de datos funciona
- [ ] Validación de campos funciona
- [ ] Selección de envío funciona
- [ ] Cálculo de envío correcto
- [ ] Resumen de pedido correcto
- [ ] Confirmar pedido crea orden
- [ ] Stock se descuenta correctamente
- [ ] Redirección a confirmación funciona

### 🔐 Autenticación

#### Registro
- [ ] Formulario de registro funciona
- [ ] Validación de email funciona
- [ ] Validación de contraseña funciona
- [ ] Usuario se crea en Supabase Auth
- [ ] Usuario se crea en app_users
- [ ] Rol 'cliente' se asigna por defecto

#### Login
- [ ] Login con email/password funciona
- [ ] Sesión persiste
- [ ] Redirección después de login funciona
- [ ] Logout funciona

### 👨‍💼 Dashboard Administrativo

#### Acceso
- [ ] Solo usuarios con rol 'admin' pueden acceder
- [ ] URL `/admin` protegida
- [ ] Redirección si no autorizado

#### Dashboard Principal
- [ ] Estadísticas se muestran correctamente
- [ ] Total de productos correcto
- [ ] Total de pedidos correcto
- [ ] Ingresos totales correctos
- [ ] Gráfico de pedidos por estado funciona
- [ ] Pedidos recientes aparecen
- [ ] Productos con stock bajo aparecen

#### Gestión de Productos
- [ ] Listado de productos funciona
- [ ] Búsqueda de productos funciona
- [ ] Filtro por estado funciona
- [ ] Crear producto funciona
- [ ] Subir imágenes funciona (Storage)
- [ ] Editar producto funciona
- [ ] Agregar variantes funciona
- [ ] Publicar/ocultar producto funciona
- [ ] Eliminar producto funciona
- [ ] Auditoría registra cambios

#### Gestión de Pedidos
- [ ] Listado de pedidos funciona
- [ ] Detalle de pedido completo
- [ ] Cambiar estado funciona
- [ ] Filtros por estado funcionan
- [ ] Búsqueda por número funciona
- [ ] Historial de cambios visible

#### Gestión de Usuarios
- [ ] Listado de usuarios funciona
- [ ] Crear usuario funciona
- [ ] Asignar roles funciona
- [ ] Bloquear/desbloquear funciona
- [ ] Búsqueda funciona

#### Gestión de Categorías
- [ ] Listado de categorías funciona
- [ ] Crear categoría funciona
- [ ] Editar categoría funciona
- [ ] Categorías jerárquicas funcionan
- [ ] Eliminar categoría funciona

#### Gestión de Marcas
- [ ] Listado de marcas funciona
- [ ] Crear marca funciona
- [ ] Editar marca funciona
- [ ] Subir logo funciona
- [ ] Eliminar marca funciona

#### Gestión de Cupones
- [ ] Listado de cupones funciona
- [ ] Crear cupón funciona
- [ ] Validación de vigencia funciona
- [ ] Límite de uso funciona
- [ ] Editar cupón funciona
- [ ] Desactivar cupón funciona

#### Gestión de Banners
- [ ] Listado de banners funciona
- [ ] Crear banner funciona
- [ ] Subir imagen funciona
- [ ] Orden de visualización funciona
- [ ] Activar/desactivar funciona
- [ ] Eliminar banner funciona

#### Reportes
- [ ] Reporte de ventas por fecha funciona
- [ ] Top productos se muestra
- [ ] Top categorías se muestra
- [ ] Gráficos se renderizan correctamente
- [ ] Exportar a CSV funciona (si implementado)

### 🗄️ Base de Datos

#### Migraciones
- [ ] 00_schema.sql ejecutado correctamente
- [ ] 01_rls.sql ejecutado correctamente
- [ ] 02_seed.sql ejecutado correctamente
- [ ] 03_storage.sql ejecutado correctamente
- [ ] Todas las tablas creadas
- [ ] Índices creados
- [ ] Triggers funcionando

#### RLS (Row Level Security)
- [ ] Políticas de products activas
- [ ] Público solo ve productos publicados
- [ ] Admin puede ver todos los productos
- [ ] Políticas de carts activas
- [ ] Usuario solo ve su carrito
- [ ] Políticas de orders activas
- [ ] Usuario solo ve sus pedidos
- [ ] Admin puede ver todos los pedidos

#### Storage
- [ ] Bucket 'products' creado
- [ ] Política de lectura pública funciona
- [ ] Política de escritura solo admin funciona
- [ ] Imágenes se suben correctamente
- [ ] URLs públicas funcionan

#### Seed Data
- [ ] 30+ productos cargados
- [ ] 6+ categorías cargadas
- [ ] 6 marcas cargadas
- [ ] 10 pedidos de ejemplo cargados
- [ ] 3 cupones cargados
- [ ] 2 banners cargados
- [ ] Usuarios demo creados

### 🚀 Despliegue

#### GitHub
- [ ] Repositorio creado
- [ ] Código subido
- [ ] Secrets configurados
- [ ] Workflows funcionando

#### Supabase
- [ ] Proyecto creado
- [ ] Base de datos provisionada
- [ ] Storage configurado
- [ ] Auth configurado
- [ ] RLS activado

#### Render
- [ ] Servicio web creado
- [ ] Variables de entorno configuradas
- [ ] Build exitoso
- [ ] Deploy exitoso
- [ ] Health check responde
- [ ] Aplicación accesible

### 🔒 Seguridad

- [ ] CSRF protection activo
- [ ] Rate limiting configurado
- [ ] RLS activo en todas las tablas
- [ ] Secrets no expuestos en código
- [ ] HTTPS en producción
- [ ] Validación de inputs
- [ ] Sanitización de datos

### 📱 Responsive & UX

- [ ] Diseño responsive en móvil
- [ ] Diseño responsive en tablet
- [ ] Diseño responsive en desktop
- [ ] Navegación móvil funciona
- [ ] Imágenes optimizadas
- [ ] Carga rápida
- [ ] Animaciones suaves

### 🌐 SEO & Accesibilidad

- [ ] Meta tags configurados
- [ ] Open Graph tags configurados
- [ ] Títulos descriptivos
- [ ] Alt text en imágenes
- [ ] Estructura semántica HTML
- [ ] Contraste de colores adecuado
- [ ] Navegación por teclado funciona

### 📧 Integraciones

- [ ] WhatsApp link funciona
- [ ] Mensaje prellenado correcto
- [ ] Email notifications (si configurado)
- [ ] Pagos sandbox funcionan

## 🎯 Criterios de Aceptación Final

### ✅ Mínimo para Producción

1. **Tienda funcional**: Catálogo visible, carrito funciona, checkout completa pedidos
2. **Dashboard operativo**: Admin puede gestionar productos, pedidos y usuarios
3. **Seguridad**: RLS activo, autenticación funciona, roles aplicados
4. **Despliegue**: App en línea en Render, accesible públicamente
5. **Datos**: Catálogo inicial cargado (30+ productos)
6. **Storage**: Imágenes se suben y muestran correctamente

### 🚀 Listo para Escalar

7. **CI/CD**: Deploys automáticos funcionando
8. **Tests**: Cobertura ≥70%
9. **Monitoreo**: Health check respondiendo
10. **Documentación**: README permite setup sin ayuda

## 📝 Notas de Prueba

### Usuarios de Prueba
- **Admin**: admin@labodegona.gt / Admin#2025!
- **Cliente**: cliente@labodegona.gt / Cliente#2025!

### URLs Importantes
- **Tienda**: https://tu-app.onrender.com
- **Admin**: https://tu-app.onrender.com/admin
- **Health**: https://tu-app.onrender.com/health
- **API Docs**: Postman collection incluida

### Comandos Útiles

```bash
# Verificar migraciones
python manage.py db-status

# Crear admin
python manage.py create-admin --email admin@labodegona.gt --password Admin#2025!

# Cargar seed
python manage.py seed

# Tests
pytest --cov=app

# Verificar health
curl https://tu-app.onrender.com/health
```

## 🐛 Reporte de Problemas

Si encuentras algún problema durante la verificación:

1. Revisa los logs en Render
2. Verifica las variables de entorno
3. Confirma que las migraciones se ejecutaron
4. Verifica políticas RLS en Supabase
5. Revisa la documentación en README.md

---

**Fecha de verificación**: _____________

**Verificado por**: _____________

**Estado**: [ ] Aprobado [ ] Requiere correcciones

**Notas adicionales**:
