from .models import Copia, Socio, Prestamo, Libro
from django.db import models

class GestorPrestamos(object):

    def getPrestados(**kwargs):
        #print(kwargs)
        return (Prestamo.objects.filter(**kwargs))

    def __str__(self):
        return (str(self.Isbn)+", "+self.Titulo)
    #def was_published_recently(self):
     #   return self.pub_date >= timezone.now()-datetime.timedelta(days=1)

class GestorSocios(object):

    def getSocios(**kwargs):
        return (Socio.objects.filter(**kwargs))

    def get(**kwargs):
        return (Socio.objects.get(**kwargs))

class GestorCopias(object):

    def getCopias(**kwargs):
        return (Copia.objects.filter(**kwargs))

    def getCopiaDisponible(Isbn):
        listaCopia = GestorCopias.getCopias(Isbn=Isbn,Prestado=False)
        if listaCopia:
            return listaCopia[0]
        else:
            return "No hay copias disponibles"