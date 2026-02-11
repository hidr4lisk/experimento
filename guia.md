# Guía de Setup - Django App para Organizar Temas

## Objetivo
Crear una aplicación Django para organizar temas con vistas de login para:
- ADMIN
- user1, user2, user3

---

## Paso 1: Plan de Trabajo

### 1. Crear el entorno virtual
```bash
# En la carpeta del proyecto
python3 -m venv venv

# Activar el entorno
source venv/bin/activate  # En Linux/Mac
```

### 2. Instalar dependencias
```bash
# Actualizar pip
pip install --upgrade pip

# Instalar Django
pip install django

# (Opcional pero recomendado) crear requirements.txt
pip freeze > requirements.txt
```

### 3. Crear el proyecto y la app
```bash
# Crear proyecto Django
django-admin startproject nombre_del_proyecto .

# Crear una app para tu aplicación
python manage.py startapp nombre_app
```

### 4. Configurar la base de datos
- Ejecutar migraciones: `python manage.py migrate`
- Crear un superusuario (admin): `python manage.py createsuperuser`

### 5. Crear usuarios adicionales
- Opción A: Desde la terminal con un script
- Opción B: Desde el panel de admin de Django

### 6. Crear la vista de login
- Crear templates (HTML)
- Configurar URLs
- Usar vistas class-based (`LoginView` de Django) o function-based

---

## Paso 2: Problemas Comunes - Venv no funciona

**Problema**: El venv "apunta a otra ruta" después de clonar el repositorio

**Causa**: El venv no es portable porque guarda rutas hardcodeadas (rutas absolutas)

### Solución

#### Opción 1: Limpiar y crear uno nuevo (Recomendado)
```bash
# 1. Eliminar el venv antiguo
rm -rf venv

# 2. Crear uno nuevo en la ruta actual
python3 -m venv venv

# 3. Activar
source venv/bin/activate
```

#### Opción 2: Regenerar el venv sin eliminarlo
```bash
# Desactivar si está activo
deactivate

# Regenerar
python3 -m venv --upgrade venv

# Activar
source venv/bin/activate
```

---

## Paso 3: Crear Usuarios (user1 y user2)

Dos opciones para crear usuarios sin permisos de administrador:

### Opción A: Usar el shell interactivo de Django

```bash
python manage.py shell
```

Una vez dentro del shell:
```python
from django.contrib.auth.models import User

# Crear user1
User.objects.create_user(username='user1', password='password_user1', email='user1@example.com')

# Crear user2
User.objects.create_user(username='user2', password='password_user2', email='user2@example.com')

# Salir del shell
exit()
```

### Opción B: Crear un script Python

Crea un archivo `crear_usuarios.py` en la raíz del proyecto:
```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nombre_del_proyecto.settings')
django.setup()

from django.contrib.auth.models import User

usuarios = [
    {'username': 'user1', 'password': 'password_user1', 'email': 'user1@example.com'},
    {'username': 'user2', 'password': 'password_user2', 'email': 'user2@example.com'},
]

for usr in usuarios:
    User.objects.create_user(**usr)
    print(f"Usuario {usr['username']} creado")
```

Luego ejecuta: `python crear_usuarios.py`

---

## Paso 4: Vista de Login

### 1. Crear la carpeta de templates

```bash
mkdir -p nombre_app/templates/nombre_app
```

### 2. Crear el template de login

Archivo: `nombre_app/templates/nombre_app/login.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h1>Iniciar Sesión</h1>
    
    {% if form.non_field_errors %}
        <p style="color: red;">{{ form.non_field_errors }}</p>
    {% endif %}
    
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Login</button>
    </form>
</body>
</html>
```

### 3. Crear la view en `nombre_app/views.py`

```python
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'nombre_app/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('nombre_app:home')  # Cambia según tu app
```

### 4. Configurar URLs - `nombre_app/urls.py`

Crea este archivo si no existe:
```python
from django.urls import path
from . import views

app_name = 'nombre_app'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
]
```

### 5. Incluir URLs en el proyecto - `nombre_del_proyecto/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('nombre_app.urls')),
]
```

### 6. Configurar settings.py

En `nombre_del_proyecto/settings.py`:

1. Asegurate que `nombre_app` esté en `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'nombre_app',  # ← Agrega esto
]
```

2. Al final del archivo agrega:
```python
LOGIN_URL = 'nombre_app:login'
LOGIN_REDIRECT_URL = 'nombre_app:home'
```

---

## Próximos pasos
(Se actualizará conforme avancemos)
