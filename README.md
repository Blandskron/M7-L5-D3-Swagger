# 🏫 API Escuela - Sistema de Gestión Escolar

Un backend robusto y escalable desarrollado con **Django** y **Django REST Framework**, diseñado para la gestión académica de estudiantes, cursos y matrículas. El proyecto incluye documentación automática con Swagger, manejo de imágenes de perfil, despliegue dockerizado y pruebas automatizadas.

## ✨ Características Principales

* **CRUD Completo:** Gestión integral de `Alumnos`, `Cursos` y `Matrículas`.
* **Filtros Avanzados:** Búsquedas y filtros en la API utilizando `django-filter`.
* **Documentación Interactiva:** OpenAPI/Swagger generado automáticamente mediante `drf-spectacular`. Redirección automática de 404 a la documentación.
* **Manejo de Archivos:** Soporte nativo para subida de fotos de perfil usando peticiones `multipart/form-data`.
* **Entorno de Producción:** Configurado con `gunicorn` para el servidor WSGI y `whitenoise` para una entrega eficiente de archivos estáticos.
* **Docker Ready:** Preparado para despliegue continuo con `Dockerfile` y `docker-compose.yml`, incluyendo orquestación con PostgreSQL.
* **Pruebas Automatizadas:** Cobertura de pruebas unitarias y de integración utilizando el `APITestCase` nativo.

## 🛠️ Stack Tecnológico

* **Python 3.12**
* **Django 6.0+**
* **Django REST Framework (DRF)**
* **PostgreSQL** (Base de datos en producción/Docker)
* **Docker & Docker Compose**

## 🚀 Instalación y Desarrollo Local

### 1. Clonar y configurar el entorno virtual
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto basándote en la siguiente configuración (ajusta los datos de tu base de datos local si no usas SQLite/Docker localmente):
```env
SECRET_KEY=tu_clave_secreta_local_muy_segura
DEBUG=True
DB_NAME=escuela_db
DB_USER=postgres
DB_PASSWORD=admin1234
DB_HOST=localhost
DB_PORT=5432
```

### 4. Migraciones y ejecución
```bash
python manage.py migrate
python manage.py runserver
```

## 🐳 Despliegue con Docker (Recomendado)

El proyecto está completamente dockerizado. Para levantar el entorno de producción que incluye la API web y PostgreSQL:

```bash
docker-compose up -d --build
```

El script de entrada (`docker-entrypoint.sh`) se encargará automáticamente de:
1. Aplicar las migraciones pendientes a PostgreSQL.
2. Recolectar archivos estáticos para la caché de `whitenoise`.
3. Crear un superusuario (`admin` / `admin1234` por defecto configurable en `.env`).
4. Levantar la aplicación con Gunicorn de manera optimizada en el puerto `8000`.

## 📚 Uso de la API y Documentación

Una vez levantado el servidor, puedes acceder a las siguientes URLs:

* **Swagger UI:** http://localhost:8000/docs/schema/swagger-ui/
* **ReDoc:** http://localhost:8000/docs/schema/redoc/
* **Rutas API Principales:** `/api/alumnos/`, `/api/cursos/`, `/api/matriculas/`

## 🧪 Ejecutar Pruebas
Para verificar la integridad del código, ejecuta la suite de tests automatizados (los archivos multimedia se simulan en memoria sin afectar tu equipo):
```bash
python manage.py test
```
