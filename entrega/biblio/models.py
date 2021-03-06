from django.db import models
from datetime import datetime

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

    
class Copia(models.Model):
    Isbn = models.ForeignKey(Libro)
    Inventario = models.AutoField(primary_key=True)
    Prestado = models.BooleanField(default=False)
    def __str__(self):
        return(str(self.Inventario)+" "+str(self.Isbn))


class Socio(models.Model):
    Id_socio = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=20)
    Apellido = models.CharField(max_length=20)
    Email = models.EmailField()
    Fecha_nac = models.DateField(unique=False)
    Estado_moroso = models.BooleanField(default=False)
    def __str__(self):
        return (str(self.Id_socio)+", "+self.Nombre+" "+self.Apellido)
    def get_prestamos(self):
        lista=self.prestamo_set.all()
        return(lista)
    
    
class Prestamo(models.Model):
    Inventario = models.ForeignKey(Copia)
    Id_socio = models.ForeignKey(Socio)
    Id_prestamo = models.AutoField(primary_key=True)
    Fecha_prestamo = models.DateField(unique=False,null=False)
    Estado = models.CharField(max_length=15,default='Pendiente') # Los estados son o Pendiente o Terminado

    def Calcular_Fecha_devolucion(self):
        if type(self.Fecha_prestamo) == str:
            fechap = datetime.datetime.strptime(self.Fecha_prestamo, '%Y-%m-%d')
        else:
            fechap = self.Fecha_prestamo
        Fecha_devolucion = fechap + timedelta(days=7)
        if type(Fecha_devolucion) == datetime.datetime:
            Fecha_devolucion = datetime.datetime.date(Fecha_devolucion)
        return (Fecha_devolucion)

    def estaDemorado(self):
        return (self.Calcular_Fecha_devolucion() <= datetime.date.today())



    def __str__(self):
        return (str(self.Id_socio)+", "+str(self.Calcular_Fecha_devolucion())+", "+str(self.Inventario))