# En la carpeta del proyecto
python3 -m venv venv

# Activar el entorno
source venv/bin/activate  # En Linux/Mac
# o si usas Windows: venv\Scripts\activate

# si hay que clonar el repositorio

# 1. Eliminar el venv antiguo
rm -rf venv

# 2. Crear uno nuevo en la ruta actual
python3 -m venv venv

# 3. Activar
source venv/bin/activate

# Actualizar pip
pip install --upgrade pip

# Instalar Django
pip install django

# (Opcional pero recomendado) crear requirements.txt
pip freeze > requirements.txt

# Crear proyecto Django
django-admin startproject nombre_del_proyecto .

# Crear una app para tu aplicación
python manage.py startapp nombre_app

4. Configurar la base de datos
Ejecutar migraciones: python manage.py migrate
Crear un superusuario (admin): python manage.py createsuperuser

5. Crear usuarios adicionales
Dos opciones:

Opción A: Desde la terminal con un script
Opción B: Desde el panel de admin de Django

6. Crear la vista de login
Crear templates (HTML)
Configurar URLs
Usar vistas class-based (LoginView de Django) o function-based