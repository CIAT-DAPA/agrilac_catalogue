# AgriLAC Catalogue

Este repositorio contiene el proyecto de AgriLAC Catalogue desarrollado con Django y Wagtail. El proyecto incluye un catalogo de metadatos de datasets de datos históricos sobre variables como precipitaciones, temperatura, humedad y otros indicadores agroclimáticos, esenciales para la planificación agrícola y la gestión de riesgos.

## ⚙️ Requisitos

- Python 3.10
- Django 4.2
- Wagtail 6.2
- Base de datos (SQLite por defecto)

## 🔧 Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/CIAT-DAPA/agrilac_catalogue
   cd agrilac_catalogue/src
   ```

2. Crea y activa un entorno virtual:

   ```bash
   python -m venv env
   source env/bin/activate  # En Windows usa `env\Scripts\activate`
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Ejecución del Proyecto

### Sin migraciones y base de datos

Si se baja el proyecto sin las migraciones y la base de datos, se deben correr los siguientes comandos:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
python manage.py createsuperuser
```

De salir errores de dependencias circulares a la hora de correr makemigrations, se debe hacer las migraciones modelo por modelo (comentar y descomentar los modelos en los archivos models.py) de aquellos que no dependan de otros primero

### Con migraciones y base de datos (recomendado)

Si se baja el proyecto con las migraciones y la base de datos, solo se debe correr:

```bash
python manage.py runserver
```
