# Contexto del Proyecto para Asistentes de IA (Gemini / Cursor / Copilot)

Este archivo proporciona contexto técnico y convenciones de codificación para este proyecto backend. Al sugerir código o refactorizaciones, asegúrate de seguir estas reglas.

## Arquitectura General
- **Framework Principal:** Django 6.0.3 y Django Rest Framework (DRF) 3.17+.
- **Base de Datos:** PostgreSQL (vía `psycopg2-binary`).
- **Gestión de Entorno:** `.env` usando `python-dotenv`.
- **Servidor WSGI:** `gunicorn` para entornos de producción.
- **Archivos Estáticos:** Gestionados con `whitenoise` usando `CompressedManifestStaticFilesStorage`.

## Modelos y Dominio (`escuela/models.py`)
- **Alumno:** Representa estudiantes. Contiene `nombre`, `apellido`, `email` y `foto_perfil` (ImageField).
- **Curso:** Representa cursos disponibles. Contiene `nombre` y `descripcion`.
- **Matricula:** Tabla intermedia con `unique_together` para relacionar `Alumno` y `Curso`.

## Convenciones de la API (`escuela/views.py` y `escuela/serializers.py`)
- Todas las vistas utilizan `ModelViewSet` y enrutadores automáticos (`DefaultRouter`).
- Filtros de DRF habilitados mediante `django_filters`.
- **Subida de Archivos:** Las peticiones que incluyen subida de imágenes usan `parser_classes = (MultiPartParser, FormParser, JSONParser)`. Se debe usar `@extend_schema` modificando la propiedad `request={"multipart/form-data": ...}` para soportar la visualización en Swagger.

## Documentación de API (`docs/urls.py`)
- Utilizamos `drf-spectacular` (OpenAPI 3).
- Los decoradores `@extend_schema_view` y `@extend_schema` son obligatorios para detallar `summary`, `description` y agrupar por `tags` cada endpoint generado.
- La ruta principal del proyecto (`/`) y los errores `404` están configurados para redirigir a `/docs/schema/swagger-ui/`.

## Despliegue y Docker
- Se utiliza `docker-compose.yml` que orquesta un contenedor `web` y un `db` (Postgres 15).
- El proyecto usa un script de entrada (`docker-entrypoint.sh`) que:
  1. Ejecuta migraciones (`migrate`).
  2. Recolecta estáticos (`collectstatic`).
  3. Crea un superusuario basado en variables de entorno.
  4. Lanza Gunicorn.

## Reglas de Codificación
1. Los comentarios y docstrings deben estar en Español.
2. Mantener `requirements.txt` actualizado si se agregan nuevas dependencias.
3. Escribir tests usando `APITestCase` de DRF y no depender de librerías externas (solo Django Test nativo). Validar carga de archivos usando `PIL.Image` en memoria.
