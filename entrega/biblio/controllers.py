from .models import Copia, Socio, Prestamo, Libro
from django.db import models

class GestorPrestamos(object):

    def getPrestados1():
        return (Prestamo.objects.filter(Estado='Pendiente'))

    def getPrestados(**kwargs):
        #print(kwargs)
        return (Prestamo.objects.filter(**kwargs))

    def __str__(self):
        return (str(self.Isbn)+", "+self.Titulo)
    #def was_published_recently(self):
     #   return self.pub_date >= timezone.now()-datetime.timedelta(days=1)

