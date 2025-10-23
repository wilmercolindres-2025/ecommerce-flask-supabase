# Guía de Contribución

¡Gracias por tu interés en contribuir a este proyecto!

## Cómo Contribuir

### 1. Fork el Proyecto

Haz fork del repositorio y clónalo localmente:

```bash
git clone https://github.com/tu-usuario/ecommerce-flask-supabase.git
cd ecommerce-flask-supabase
```

### 2. Crear una Rama

Crea una rama para tu feature o bugfix:

```bash
git checkout -b feature/nueva-funcionalidad
# o
git checkout -b fix/corregir-bug
```

### 3. Hacer Cambios

- Sigue las convenciones de código del proyecto
- Escribe tests para nuevas funcionalidades
- Actualiza la documentación si es necesario

### 4. Ejecutar Tests

Asegúrate de que todos los tests pasen:

```bash
pytest
```

### 5. Commit

Usa mensajes de commit descriptivos:

```bash
git commit -m "feat: agregar funcionalidad de cupones"
git commit -m "fix: corregir cálculo de envío"
git commit -m "docs: actualizar README"
```

### 6. Push y Pull Request

```bash
git push origin feature/nueva-funcionalidad
```

Luego abre un Pull Request en GitHub.

## Estándares de Código

- Python: Sigue PEP 8
- JavaScript: Usa ES6+
- CSS: Usa Tailwind CSS
- Commits: Conventional Commits

## Reportar Bugs

Abre un issue con:
- Descripción del bug
- Pasos para reproducir
- Comportamiento esperado vs actual
- Screenshots si aplica

## Solicitar Features

Abre un issue describiendo:
- La funcionalidad deseada
- Casos de uso
- Beneficios para el proyecto
