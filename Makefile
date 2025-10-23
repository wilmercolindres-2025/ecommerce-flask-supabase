.PHONY: help dev test seed deploy lint format clean install build

help:
	@echo "Comandos disponibles:"
	@echo "  make install    - Instalar dependencias"
	@echo "  make dev        - Ejecutar en desarrollo"
	@echo "  make build      - Compilar assets"
	@echo "  make test       - Ejecutar tests"
	@echo "  make seed       - Cargar datos de ejemplo"
	@echo "  make lint       - Ejecutar linter"
	@echo "  make format     - Formatear código"
	@echo "  make clean      - Limpiar archivos temporales"
	@echo "  make deploy     - Desplegar (via GitHub Actions)"

install:
	pip install -r requirements.txt
	npm install

dev:
	@echo "Iniciando servidor de desarrollo..."
	flask run --debug

build:
	@echo "Compilando assets..."
	npm run build

test:
	@echo "Ejecutando tests..."
	pytest

seed:
	@echo "Cargando datos de ejemplo..."
	python manage.py seed

lint:
	@echo "Ejecutando linter..."
	flake8 app tests
	ruff check app tests

format:
	@echo "Formateando código..."
	black app tests

clean:
	@echo "Limpiando archivos temporales..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info

deploy:
	@echo "El despliegue se realiza automáticamente via GitHub Actions"
	@echo "Haz push a la rama 'main' para desplegar"
