from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Copia, Socio, Prestamo, Libro
from django.template.context_processors import request

# Create your views here.

def index(request):
    return HttpResponse("Aqui ira un menu con links.")

def prestamo(request,Id_socio,Isbn):
    return HttpResponse("implementa prestamo para el socio: "+ Id_socio +" para libro: "+Isbn)

def devolucion(request,Id_socio,Inventario):
    return HttpResponse("Implementa devolucion para el socio: "+ Id_socio +" para copia: "+Inventario)

def info_socio(request,Id_socio):
    socio_inst=get_object_or_404(Socio, pk=Id_socio)
    return HttpResponse("devuelve informacion del socio "+ str(socio_inst) +"<br/>" + str(socio_inst.get_prestamos()) )

def info_copia(request,Inventario):
    return HttpResponse("devuelve informacion del copia "+Inventario)

def info_libro(request,Isbn):
    libro_inst = get_object_or_404(Libro, pk=Isbn)
    #return render(request, '/detail.html', {'question': question})
    return HttpResponse("devuelve informacion del libro "+str(libro_inst))

def morosos(request):
    return HttpResponse("devuelve lista de moroso")

def futuros_morosos(request):
    return HttpResponse("devuelve lista de futuros morosos")

def prestamo_fecha(request,fecha):
    return HttpResponse("devuelve lista de libros prestados en determinada fecha "+fecha)
    #Revisar que el input sea una fecha valida

