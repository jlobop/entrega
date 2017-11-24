from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Copia, Socio, Prestamo, Libro
from django.template import loader
import datetime
from .controllers import *
from .forms import *
import time

from django.template.context_processors import request

# Create your views here.

def index(request):
    print(request)

    if request.method != "GET":
        return HttpResponse("chau")

    #formLibro=LibroForm(request.GET)
    #print(formLibro)
    #print(request.GET)

    if 'solicitud' in request.GET.keys():

        solicitud = request.GET['solicitud']
        print(solicitud)
        if solicitud == 'info_libro':
            #return redirect('info_libro',request.GET['Isbn'])
            return HttpResponseRedirect("/biblio/libro/"+request.GET['Isbn'])



    formSocio = SocioForm()
    formLibro = LibroForm()

    template = loader.get_template('biblio/index.html')
    context = {
        'formSocio': formSocio,
        'formLibro': formLibro,
    }
    #print(template.render(context, request))
    return render(request,'biblio/index.html',context)
    #return HttpResponse(template.render(context, request))


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
    prestamo_lista = GestorPrestamos.getPrestados(Id = Id_socio)

    template = loader.get_template('biblio/info_socio.html')
    context = {
        'socio': socio_inst,
        'prestamo_lista': prestamo_lista,
    }
    return HttpResponse(template.render(context, request))
    #return HttpResponse("devuelve informacion del socio "+ str(socio_inst) +"<br/>" + str(socio_inst.get_prestamos()))

def info_copia(request,Inventario):
    copia_inst = get_object_or_404(Copia, pk = Inventario)
    if copia_inst.Prestado == False:
        template = loader.get_template('biblio/info_copia.html')
        context = {
            'copia': copia_inst,
        }
        return HttpResponse(template.render(context, request))

    prestamo_inst = GestorPrestamos.getPrestados(Inventario = Inventario, Estado = 'Pendiente')[0]
    socio_inst = prestamo_inst.Id
    print(socio_inst)
    template = loader.get_template('biblio/info_copia.html')
    context = {
        'copia': copia_inst,
        'socio': socio_inst,
    }
    return HttpResponse(template.render(context, request))

def info_libro(request,Isbn):
    libro_inst = get_object_or_404(Libro, pk=Isbn)

    copia_lista = GestorCopias.getCopias(Isbn = Isbn)

    template = loader.get_template('biblio/info_libro.html')
    context = {
        'libro': libro_inst,
        'copia_lista': copia_lista,
    }
    return HttpResponse(template.render(context, request))

def morosos(request):
    lista_socio_moroso = [str(i) for i in GestorSocios.getSocios(Estado_moroso=True)]
    template = loader.get_template('biblio/morosos.html')
    context = {
        'lista_socio_moroso': lista_socio_moroso,
    }
    return HttpResponse(template.render(context, request))

def futuros_morosos(request):
    lista_pendientes = GestorPrestamos.getPrestados(Estado = 'Pendiente')
    #lista = list(map(lambda foo: foo.estaDemorado() ,lista_pendientes))
    lista_prestamos_atrasados = list(filter(lambda futuro_moroso: futuro_moroso.estaDemorado(), lista_pendientes))

    #[new_list.append(x) for x in list if x not in new_list]

    lista_futuros_morosos = []
    [lista_futuros_morosos.append(prestamo.Id) for prestamo in lista_prestamos_atrasados if prestamo.Id not in lista_futuros_morosos]

    template = loader.get_template('biblio/futuros_morosos.html')
    context = {
        'lista_futuros_morosos': lista_futuros_morosos,
    }
    return HttpResponse(template.render(context, request))
    #return HttpResponse("devuelve lista de futuros morosos"+'<br>'+'<br>'.join(str(i) for i in lista_futuros_morosos))

def prestamo_fecha(request,fecha):
    try:
        fechaValidada = datetime.datetime.strptime(fecha, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Formato de fecha incorrecto, debe ser YYYY-MM-DD")

    lista=[str(i) for i in GestorPrestamos.getPrestados(Fecha_prestamo=fecha)]

    template = loader.get_template('biblio/prestamo_fecha.html')
    context = {
        'fecha': fecha,
        'listaPrestamo': lista,
    }
    return HttpResponse(template.render(context, request))
