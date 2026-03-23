from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
from .models import Alumno, Curso, Matricula

class EscuelaAPITests(APITestCase):
    
    def setUp(self):
        """
        Se ejecuta antes de cada prueba.
        Preparamos algunos datos iniciales en la base de datos de pruebas.
        """
        self.curso = Curso.objects.create(nombre="Django Básico", descripcion="Curso inicial de Django")
        self.alumno = Alumno.objects.create(nombre="Juan", apellido="Pérez", email="juan@example.com")
        self.matricula = Matricula.objects.create(alumno=self.alumno, curso=self.curso)

    # --- PRUEBAS DE MODELOS ---
    def test_modelos_str(self):
        """Prueba que los métodos __str__ de los modelos devuelvan el formato correcto"""
        self.assertEqual(str(self.curso), "Django Básico")
        self.assertEqual(str(self.alumno), "Juan Pérez")
        self.assertEqual(str(self.matricula), "Matrícula: Juan Pérez en Django Básico")

    # --- PRUEBAS DE CURSO ---
    def test_listar_cursos(self):
        response = self.client.get('/api/cursos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nombre'], "Django Básico")

    def test_crear_curso(self):
        data = {'nombre': 'Python Avanzado', 'descripcion': 'POO y más'}
        response = self.client.post('/api/cursos/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Curso.objects.count(), 2)

    # --- PRUEBAS DE ALUMNO ---
    def test_listar_alumnos(self):
        response = self.client.get('/api/alumnos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_crear_alumno_con_imagen(self):
        """Prueba la creación de un alumno subiendo una foto simulada"""
        # Creamos una imagen 1x1 real en memoria usando Pillow
        image = Image.new('RGB', (1, 1), color=(255, 0, 0))
        img_io = io.BytesIO()
        image.save(img_io, format='JPEG')
        img_content = img_io.getvalue()
        
        foto_falsa = SimpleUploadedFile(
            "foto_perfil.jpg", 
            img_content, 
            content_type="image/jpeg"
        )
        
        data = {
            'nombre': 'Ana',
            'apellido': 'Gómez',
            'email': 'ana@example.com',
            'foto_perfil': foto_falsa
        }
        
        # Usamos format='multipart' porque estamos enviando un archivo
        response = self.client.post('/api/alumnos/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Alumno.objects.count(), 2)
        
        nuevo_alumno = Alumno.objects.get(email='ana@example.com')
        self.assertTrue(bool(nuevo_alumno.foto_perfil)) # Comprueba que sí se guardó un archivo

    # --- PRUEBAS DE MATRÍCULA ---
    def test_listar_matriculas(self):
        response = self.client.get('/api/matriculas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_crear_matricula(self):
        nuevo_curso = Curso.objects.create(nombre="DRF Intermedio")
        data = {'alumno': self.alumno.id, 'curso': nuevo_curso.id}
        
        response = self.client.post('/api/matriculas/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Matricula.objects.count(), 2)

    def test_matricula_duplicada_falla(self):
        """Prueba que un alumno no pueda matricularse dos veces en el mismo curso"""
        data = {'alumno': self.alumno.id, 'curso': self.curso.id}
        response = self.client.post('/api/matriculas/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
