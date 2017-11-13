from django.db import models

# Create your modefrom django.db import models
from django.utils import timezone
import datetime
from django.db.models.fields.related import ForeignKey
from datetime import timedelta

# Create your models here.

class Libro(models.Model):
    Isbn = models.BigIntegerField(primary_key=True)
    Titulo= models.CharField(max_length=60)
    Autor=models.CharField(max_length=60)
    Fecha_ingreso = models.DateTimeField(unique=False)
    def __str__(self):
        return (str(self.id)+", "+self.Titulo)
    #def was_published_recently(self):
     #   return self.pub_date >= timezone.now()-datetime.timedelta(days=1)
    
class Copia(models.Model):
    Isbn = models.ForeignKey(Libro)
    Inventario= models.IntegerField(unique=True)
    Prestado=models.BooleanField(default=False)
    def __str__(self):
        return(str(self.inventario))

class Socio(models.Model):
    Id=models.AutoField(primary_key=True)
    Nombre=models.CharField(max_length=20)
    Apellido=models.CharField(max_length=20)
    Email=models.EmailField()
    Fecha_nac=models.DateTimeField(unique=False)
    Estado_moroso=models.BooleanField(default=False)
    def __str__(self):
        return (str(self.id)+", "+self.Nombre+" "+self.Apellido)

class Prestamo(models.Model):
    Inventario=models.ForeignKey(Copia)
    Id=models.ForeignKey(Socio)
    Id_prestamo=models.AutoField(primary_key=True)
    Fecha_prestamo=models.DateTimeField(unique=False,null=False)
    Estado=models.CharField(max_length=15,default='Pendiente')
    def Calcular_Fecha_devolucion(self):
        self.Fecha_devolucion = Prestamo.Fecha_prestamo + datetime.timedelta(days=7)
        #return self.Fecha_devolucion
    def __str__(self):
        return (str(self.id)+", "+self.Fecha_devolucion)
    
    
    
    

