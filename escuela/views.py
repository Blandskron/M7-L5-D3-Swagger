from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Alumno, Curso, Matricula
from .serializers import AlumnoSerializer, CursoSerializer, MatriculaSerializer

@extend_schema_view(
    list=extend_schema(summary="Listar Alumnos", description="Obtiene una lista de todos los alumnos registrados.", tags=['Alumnos']),
    retrieve=extend_schema(summary="Obtener Alumno", description="Obtiene los detalles de un alumno específico por su ID.", tags=['Alumnos']),
    create=extend_schema(
        summary="Crear Alumno",
        description="Registra un nuevo alumno en el sistema, permitiendo subir una foto de perfil.",
        tags=['Alumnos'],
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "nombre": {"type": "string"},
                    "apellido": {"type": "string"},
                    "email": {"type": "string", "format": "email"},
                    "foto_perfil": {"type": "string", "format": "binary"},
                },
                "required": ["nombre", "apellido", "email"],
            }
        }
    ),
    update=extend_schema(
        summary="Actualizar Alumno",
        description="Actualiza todos los datos de un alumno existente.",
        tags=['Alumnos'],
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "nombre": {"type": "string"},
                    "apellido": {"type": "string"},
                    "email": {"type": "string", "format": "email"},
                    "foto_perfil": {"type": "string", "format": "binary"},
                },
                "required": ["nombre", "apellido", "email"],
            }
        }
    ),
    partial_update=extend_schema(
        summary="Actualización Parcial de Alumno",
        description="Actualiza uno o más campos de un alumno.",
        tags=['Alumnos'],
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "nombre": {"type": "string"},
                    "apellido": {"type": "string"},
                    "email": {"type": "string", "format": "email"},
                    "foto_perfil": {"type": "string", "format": "binary"},
                }
            }
        }
    ),
    destroy=extend_schema(summary="Eliminar Alumno", description="Elimina un alumno del sistema.", tags=['Alumnos'])
)
class AlumnoViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer
    # Habilita multipart/form-data para que Swagger permita subir archivos (foto_perfil)
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    # Permite filtrar por ej: /api/alumnos/?nombre=Juan&email=juan@test.com
    filterset_fields = ['nombre', 'apellido', 'email']

@extend_schema_view(
    list=extend_schema(summary="Listar Cursos", description="Obtiene una lista de todos los cursos.", tags=['Cursos']),
    retrieve=extend_schema(summary="Obtener Curso", description="Obtiene los detalles de un curso por su ID.", tags=['Cursos']),
    create=extend_schema(summary="Crear Curso", description="Crea un nuevo curso.", tags=['Cursos']),
    update=extend_schema(summary="Actualizar Curso", description="Actualiza un curso existente.", tags=['Cursos']),
    partial_update=extend_schema(summary="Actualización Parcial de Curso", description="Actualiza parcialmente un curso existente.", tags=['Cursos']),
    destroy=extend_schema(summary="Eliminar Curso", description="Elimina un curso.", tags=['Cursos'])
)
class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    filterset_fields = ['nombre']

@extend_schema_view(
    list=extend_schema(summary="Listar Matrículas", description="Obtiene una lista de todas las matrículas.", tags=['Matrículas']),
    retrieve=extend_schema(summary="Obtener Matrícula", description="Obtiene los detalles de una matrícula por su ID.", tags=['Matrículas']),
    create=extend_schema(summary="Crear Matrícula", description="Registra una nueva matrícula de un alumno en un curso.", tags=['Matrículas']),
    update=extend_schema(summary="Actualizar Matrícula", description="Actualiza una matrícula existente.", tags=['Matrículas']),
    partial_update=extend_schema(summary="Actualización Parcial de Matrícula", description="Actualiza parcialmente una matrícula existente.", tags=['Matrículas']),
    destroy=extend_schema(summary="Eliminar Matrícula", description="Elimina una matrícula.", tags=['Matrículas'])
)
class MatriculaViewSet(viewsets.ModelViewSet):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
    filterset_fields = ['alumno', 'curso', 'fecha_matricula']
