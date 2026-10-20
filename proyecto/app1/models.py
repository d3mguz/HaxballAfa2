from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    url_imagen = models.URLField()
    descripcion = models.TextField()

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=128)

    def guardar_contrasena(self, contrasena):
        self.contrasena = make_password(contrasena)  # Cambiado self.contraseña por self.contrasena

    def verificar_contrasena(self, contrasena):
        return check_password(contrasena, self.contrasena)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
