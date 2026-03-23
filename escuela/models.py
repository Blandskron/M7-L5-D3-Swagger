from django.db import models


class Curso(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    foto_perfil = models.ImageField(upload_to='alumnos/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Matricula(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='matriculas')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='matriculas')
    fecha_matricula = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('alumno', 'curso') # Un alumno no puede matricularse dos veces al mismo curso

    def __str__(self):
        return f"Matrícula: {self.alumno} en {self.curso}"
