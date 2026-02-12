# Control de Asistencia y Registros

Sistema web para gestionar asistencia, vacaciones, franquicias, comisiones y razones particulares del personal.

## Características

- 🔐 **Autenticación de usuarios**: 3 roles (Admin, Emma, Pipo)
- 📊 **Tabla interactiva**: Filtrar y ordenar registros por agente, tipo y fecha
- 📅 **Calendario visual**: Visualizar registros por agente con colores diferenciados
- 👤 **Gestión de agentes**: Solo admin puede crear, editar agentes y registros
- 🔍 **Protección de datos**: Información confidencial requiere login

## Tipos de Registros

- 🟨 **Vacaciones**
- 🟪 **Franquicia**
- 🟧 **Razón Particular**
- 🟥 **Comisión**

## Instalación Local

### Requisitos
- Python 3.12+
- pip

### Setup

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/experimento.git
cd experimento

# Crear entorno virtual
python3 -m venv venv

# Activar entorno
source venv/bin/activate  # Linux/Mac
# o: venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Crear migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario (opcional)
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

Acceder en: http://localhost:8000/

## Usuarios de Prueba

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| admin   | admin     | Admin |
| emma    | emma      | Usuario |
| pipo    | pipo      | Usuario |

## Deployment en Render

### Variables de Entorno Necesarias

```
SECRET_KEY=django-insecure-change-this
DEBUG=False
ALLOWED_HOSTS=experimento-ikiy.onrender.com,localhost
DATABASE_URL=postgresql://...
```

### Pasos

1. **Conectar repositorio en Render**
   - Ir a https://render.com
   - Crear nuevo "Web Service"
   - Conectar con GitHub
   - Seleccionar este repositorio

2. **Configurar variables de entorno**
   - Environment: Python
   - Build Command: `chmod +x build.sh && ./build.sh`
   - Start Command: `gunicorn experimento.wsgi`
   - Agregar variables en "Environment"

3. **Deploy**
   - Render ejecutará automáticamente el build.sh
   - Se crearán las migraciones
   - Se recolectarán los archivos estáticos
   - La app estará disponible en la URL asignada

## Estructura del Proyecto

```
experimento/
├── experimentapp/          # Aplicación principal
│   ├── models.py          # Modelos: Agent, Record
│   ├── views.py           # Vistas y lógica
│   ├── urls.py            # Rutas
│   ├── templates/         # Templates HTML
│   └── migrations/        # Migraciones de BD
├── experimento/           # Configuración Django
│   ├── settings.py        # Configuración
│   ├── urls.py            # URLs principales
│   └── wsgi.py           # WSGI para producción
├── manage.py              # Script de Django
├── requirements.txt       # Dependencias
├── Procfile              # Configuración para Heroku/Render
└── build.sh              # Script de build
```

## Tecnologías

- Django 6.0.2
- Python 3.12
- SQLite (local) / PostgreSQL (producción)
- FullCalendar 6.1
- WhiteNoise (archivos estáticos)
- Gunicorn (servidor WSGI)

## Funcionalidades por Usuario

### Admin
- ✅ Ver tabla completa de registros
- ✅ Filtrar y ordenar
- ✅ Agregar nuevos agentes
- ✅ Editar agentes
- ✅ Crear nuevos registros
- ✅ Editar registros existentes
- ✅ Ver calendarios de agentes

### Emma / Pipo
- ✅ Ver tabla completa de registros
- ✅ Filtrar y ordenar
- ✅ Ver calendarios de agentes
- ❌ No pueden crear/editar

## Notas

- Los sábados y domingos no se consideran laborales
- Los registros solo se marcan en días de lunes a viernes
- Cada tipo de registro tiene un color único
- El calendario es interactivo y permite navegar mes/semana

## Licencia

MIT
