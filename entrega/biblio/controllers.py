from .models import Copia, Socio, Prestamo, Libro
import time
import datetime

from django.db import models

class GestorPrestamos(object):

    def getPrestados(**kwargs):
        #print(kwargs)
        return (Prestamo.objects.filter(**kwargs))

    def __str__(self):
        return (str(self.Isbn)+", "+self.Titulo)
    #def was_published_recently(self):
     #   return self.pub_date >= timezone.now()-datetime.timedelta(days=1)

    def devolver(Id_socio, Inventario):
        try:
            #prestamo = GestorPrestamos.getPrestados(Id=Id_socio, Inventario=Inventario)
            prestamo = Prestamo.objects.get(Id=Id_socio, Inventario=Inventario, Estado = 'Pendiente')

        except Exception as e:
            #print(type(e))
            #if str(type(e)) == 'biblio.models.DoesNotExist':
            return "No existe el prestamo solicitado"
            #return "Fallo algo"

        Fecha_devolucion = prestamo.Calcular_Fecha_devolucion()
        print(type(time.strftime("%Y-%m-%d")))

        quedomoroso=False
        #if Fecha_devolucion < time.strftime("%Y-%m-%d") + datetime.timedelta(days=7):
        if Fecha_devolucion < datetime.date.today():
            socio = prestamo.Id
            socio.Estado_moroso = True
            quedomoroso = True
            socio.save()

        copia = prestamo.Inventario
        copia.Prestado = False
        copia.save()

        prestamo.Estado = 'Terminado'
        prestamo.save()

        msg = "Muchas Gracias por devolver el libro!" if not quedomoroso else 'El libro se devolvio tarde, el socio quedo moroso.'
        return msg

        '''
        if type(prestamo.Fecha_prestamo) == str:
            fechap = datetime.datetime.strptime(self.Fecha_prestamo, '%Y-%m-%d')
        else:
            fechap = self.Fecha_prestamo
        Fecha_devolucion = fechap + timedelta(days=7)
        if type(Fecha_devolucion) == datetime.datetime:
            Fecha_devolucion = datetime.datetime.date(Fecha_devolucion)
        '''
        return prestamo


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
            candidata = listaCopia[0]
            candidata.Prestado = True
            candidata.save()
            return candidata
        else:
            return "No hay copias disponibles"