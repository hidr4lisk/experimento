# SIA - Control de Asistencia

Sistema Interno de Administración para la Gerencia de Planeamiento y Concesiones.

## 🚀 Características

- **Dashboard Principal**: Consulta rápida de registros de asistencia y personal.
- **Calendario por Agente**: Visualización interactiva con feriados nacionales (Argentina) integrados.
- **Gestión de Roles**:
  - **ADMIN**: Control total y administración de usuarios.
  - **EDITOR**: Gestión de agentes y registros de asistencia.
  - **LECTOR**: Consulta y visualización institucional.
- **Seguridad**: Protección de endpoints, passwords validadas y comunicación segura.

## 🛠️ Requisitos Rápidos (Docker)

La aplicación está diseñada para correr en un entorno Dockerizado.

### Despliegue con Docker Compose
```bash
docker-compose up -d --build
```
La aplicación estará disponible en `http://localhost:8000`.

### Variables de Entorno (.env)
Asegúrese de configurar las siguientes variables:
- `SECRET_KEY`: Clave única para la sesión.
- `DEBUG`: `False` en producción.
- `POSTGRES_PASSWORD`: Contraseña para la base de datos distribuida.

## 📁 Estructura del Proyecto

- `experimentapp/`: Lógica principal de la aplicación Django.
- `experimento/`: Configuración del core del proyecto.
- `scripts/`: Herramientas de backup y mantenimiento.
- `templates/`: Interfaz de usuario premium y responsiva.

---
© 2026 - Diseñado y Producido por **Federico Furgiuele**.