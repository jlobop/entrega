from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Copia, Socio, Prestamo, Libro
from django.template import loader
import datetime
from .controllers import *
import time

from django.template.context_processors import request

# Create your views here.

def index(request):
    template = loader.get_template('biblio/index.html')
    context = {
    }
    print(template.render(context, request))
    return HttpResponse(template.render(context, request))
    #return HttpResponse("Aqui ira un menu con links.")

def prestamo(request,Id_socio,Isbn):

    try:
        socio = GestorSocios.get(Id=Id_socio)
    except Exception as e:
        if type(e).__name__ == 'DoesNotExist':
            return HttpResponse("El Socio no existe " + Id_socio)
        else:
            return HttpResponse(type(e).__name__)

    if socio.Estado_moroso:
        return HttpResponse("El Socio " + Id_socio + " es moroso")

    copia = GestorCopias.getCopiaDisponible(Isbn)

    if copia == "No hay copias disponibles":
        return HttpResponse("No hay copias disponibles para " + Isbn)

    prestamo = Prestamo(Inventario = copia, Id = socio, Fecha_prestamo = str(time.strftime("%Y-%m-%d")))
    prestamo.save()

    print(prestamo)



    #Fecha_prestamo = time.strftime("%Y-%m-%d")
    return HttpResponse("implementa prestamo para el socio: "+ Id_socio +" para libro: "+Isbn)

def devolucion(request,Id_socio,Inventario):
    resultadoDevolucion = GestorPrestamos.devolver(Id_socio,Inventario)
    return HttpResponse(str(resultadoDevolucion))


def info_socio(request,Id_socio):
    socio_inst = get_object_or_404(Socio, pk=Id_socio)
    template = loader.get_template('biblio/info_socio.html')
    context = {
        'socio': socio_inst,
    }
    return HttpResponse(template.render(context, request))
    #return HttpResponse("devuelve informacion del socio "+ str(socio_inst) +"<br/>" + str(socio_inst.get_prestamos()))

def info_copia(request,Inventario):
    copia_inst = get_object_or_404(Copia, pk = Inventario)
    template = loader.get_template('biblio/info_copia.html')
    context = {
        'copia': copia_inst,
    }
    return HttpResponse(template.render(context, request))
    #return HttpResponse("devuelve informacion del copia "+Inventario)

def info_libro(request,Isbn):
    libro_inst = get_object_or_404(Libro, pk=Isbn)
    template = loader.get_template('biblio/info_libro.html')
    context = {
        'libro': libro_inst,
    }
    return HttpResponse(template.render(context, request))
    #return render(request, '/detail.html', {'question': question})
    #return HttpResponse("devuelve informacion del libro "+str(libro_inst))

def morosos(request):
    return HttpResponse("devuelve lista de moroso")

def futuros_morosos(request):
    return HttpResponse("devuelve lista de futuros morosos")

def prestamo_fecha(request,fecha):
    try:
        fechaValidada = datetime.datetime.strptime(fecha, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Formato de fecha incorrecto, debe ser YYYY-MM-DD")

    lista=[str(i) for i in GestorPrestamos.getPrestados(Fecha_prestamo=fecha)]
    lista_str = '<BR>'.join(lista)

    template = loader.get_template('biblio/prestamo_fecha.html')
    context = {
        'fecha': fecha,
        'listaPrestamo': lista,
    }
    return HttpResponse(template.render(context, request))
