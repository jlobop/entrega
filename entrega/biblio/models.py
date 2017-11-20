from django.db import models

# Create your modefrom django.db import models
from django.utils import timezone
import datetime
from django.db.models.fields.related import ForeignKey
from datetime import timedelta, date


# Create your models here.
class Libro(models.Model):
    Isbn = models.BigIntegerField(primary_key=True)
    Titulo = models.CharField(max_length=60)
    Autor = models.CharField(max_length=60)
    Fecha_ingreso = models.DateField(unique=False)
    def __str__(self):
        return (str(self.Isbn)+", "+self.Titulo)
    #def was_published_recently(self):
     #   return self.pub_date >= timezone.now()-datetime.timedelta(days=1)
    
class Copia(models.Model):
    Isbn = models.ForeignKey(Libro)
    Inventario = models.AutoField(primary_key=True)
    Prestado = models.BooleanField(default=False)
    def __str__(self):
        return(str(self.Inventario)+" "+str(self.Isbn))

class Socio(models.Model):
    Id = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=20)
    Apellido = models.CharField(max_length=20)
    Email = models.EmailField()
    Fecha_nac = models.DateField(unique=False)
    Estado_moroso = models.BooleanField(default=False)
    def __str__(self):
        return (str(self.Id)+", "+self.Nombre+" "+self.Apellido)
    def get_prestamos(self):
        lista=self.prestamo_set.all()
        return(lista)
    
class Prestamo(models.Model):
    Inventario = models.ForeignKey(Copia)
    Id = models.ForeignKey(Socio)
    Id_prestamo = models.AutoField(primary_key=True)
    Fecha_prestamo = models.DateField(unique=False,null=False)
    Estado = models.CharField(max_length=15,default='Pendiente')
    # Los estados son o Pendiente o Terminado

    #Fecha_devolucion = date(int(str(Fecha_prestamo)) + datetime.timedelta(days=7))
    
    def Calcular_Fecha_devolucion(self):
        #self.Fecha_devolucion = Prestamo.Fecha_prestamo + datetime.timedelta(days=7)
        Fecha_devolucion = self.Fecha_prestamo + timedelta(days=7)
        return (Fecha_devolucion)
    #def __init__(self):
    #    self.Calcular_Fecha_devolucion()
    def __str__(self):
        return (str(self.Id)+", "+str(self.Calcular_Fecha_devolucion())+", "+str(self.Inventario))