from .models import Copia, Socio, Prestamo, Libro
import time
import datetime

from django.db import models

class GestorPrestamos(object):

    def getPrestados(**kwargs):
        return (Prestamo.objects.filter(**kwargs))

    def devolver(Id_socio, Inventario):
        try:
            prestamo = Prestamo.objects.get(Id_socio=Id_socio, Inventario=Inventario, Estado = 'Pendiente')

        except Exception as e:
            return "No existe el prestamo solicitado"

        Fecha_devolucion = prestamo.Calcular_Fecha_devolucion()
        print(type(time.strftime("%Y-%m-%d")))

        quedomoroso=False
        if Fecha_devolucion < datetime.date.today():
            socio = prestamo.Id_socio
            socio.Estado_moroso = True
            quedomoroso = True
            socio.save()

        copia = prestamo.Inventario
        copia.Prestado = False
        copia.save()

        prestamo.Estado = 'Terminado'
        prestamo.save()

        msg = "Muchas Gracias por devolver el libro! " if not quedomoroso else 'El libro se devolvio tarde, el socio quedo moroso.'
        msg = msg + " <br><a href='/biblio/'>Volver</a>"
        return msg
        #return prestamo
    
    def __str__(self):
        return (str(self.Isbn)+", "+self.Titulo)



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