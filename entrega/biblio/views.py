from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Copia, Socio, Prestamo, Libro
from django.template import loader
import datetime
from .controllers import *
from .forms import *
import time

from django.template.context_processors import request
from time import strptime


def index(request):
    #print(request)

    urlbase='/biblio/'


    if request.method == "POST":
        if 'solicitud' in request.POST.keys():
            solicitud = request.POST['solicitud']
            
            if solicitud == 'prestamo':
                formPrestamo = PrestamoForm(request.POST)
                if formPrestamo.is_valid():
                    libro=formPrestamo.cleaned_data['Isbn']
                    socio=formPrestamo.cleaned_data['Id_socio']
                    print(libro)
                    print(socio)
                    Isbn = str(libro.Isbn)
                    Id_socio=str(socio.Id_socio)

                    return redirect(urlbase+"prestamo/" + Id_socio  + "/" + Isbn)
                else:
                    return HttpResponse('Libro o Socio no encontrado o socio inhabilitados o algun formato invalido...')                    

                    
            elif solicitud == 'devolucion':
                formDevolucion = DevolucionForm(request.POST)
                if formDevolucion.is_valid():
                    copia=formDevolucion.cleaned_data['Inventario']
                    print(copia)
                    socio=formDevolucion.cleaned_data['Id_socio']
                    print(socio)

                    Inventario = str(copia.Inventario)
                    Id_socio=str(socio.Id_socio)

                    return redirect(urlbase+"devolucion/" + Id_socio  + "/" + Inventario)
                else:
                    return HttpResponse('Libro o Socio no encontrado o socio inhabilitados o algun formato invalido...<br><a href="/biblio/">Volver</a>')                    
                    
            elif solicitud == 'alta_socio':
                formAltaSocio = AltaSocioForm(request.POST)
                if formAltaSocio.is_valid():
                    print(formAltaSocio.cleaned_data)
                    nuevo_socio = Socio(Nombre=formAltaSocio.cleaned_data['Nombre'],
                                        Apellido=formAltaSocio.cleaned_data['Apellido'],
                                        Email=formAltaSocio.cleaned_data['Email'],
                                        Fecha_nac=formAltaSocio.cleaned_data['Fecha_nac'],
                                        )
                    nuevo_socio.save()

                    return HttpResponse('Se ha dado de alta el nuevo socio: ' + str(nuevo_socio)  +' <br><a href="/biblio/">Volver</a>')
                else:
                    return HttpResponse('Datos o Formato incorrectos. Por favor revise.<br><a href="/biblio/">Volver</a>')                    
                    
            elif solicitud == 'alta_libro':
                formAltaLibro = AltaLibroForm(request.POST)
                if formAltaLibro.is_valid():
                    print(formAltaLibro.cleaned_data)
                    nuevo_libro = Libro(Isbn=formAltaLibro.cleaned_data['Isbn'],
                                        Titulo=formAltaLibro.cleaned_data['Titulo'],
                                        Autor=formAltaLibro.cleaned_data['Autor'],
                                        Fecha_ingreso=formAltaLibro.cleaned_data['Fecha_ingreso'],
                                        )
                    nuevo_libro.save()

                    [Copia(Isbn=nuevo_libro).save() for _ in range(formAltaLibro.cleaned_data['ncopias'])]

                    return HttpResponse('Se ha dado de alta el nuevo libro:  ' + str(nuevo_libro) +' <br><a href="/biblio/">Volver</a>')
                else:
                    return HttpResponse('Datos o Formato incorrectos. Por favor revise.<br><a href="/biblio/">Volver</a>')                    


    if request.method != "GET":
        return HttpResponse("Metodo no implementado. <br><a href='/biblio/'>Volver</a>")

    if 'solicitud' in request.GET.keys():
        solicitud = request.GET['solicitud']
        #print(request.GET)
        if solicitud == 'info_libro':
            formLibro=LibroForm(request.GET)
            if formLibro.is_valid():
                libro=formLibro.cleaned_data['Isbn']
                Isbn = str(libro.Isbn)
                return redirect(urlbase+"libro/" + Isbn)
            else:
                return HttpResponse('Libro no encontrado o formato invalido...<br><a href="/biblio/">Volver</a>')
                        

        elif solicitud == 'info_socio':
            Id_socio=request.GET['Id_socio']
            return HttpResponseRedirect(urlbase+"socio/" + Id_socio)
        
        
        elif solicitud == 'info_copia':
            formCopia=CopiaForm(request.GET)
            if formCopia.is_valid():
                #Isbn=request.GET['Isbn']
                copia=formCopia.cleaned_data['Inventario']
                Inventario = str(copia.Inventario)
                return redirect(urlbase+"copia/" + Inventario)
            else:
                return HttpResponse('Copia no encontrada o formato invalido...<br><a href="/biblio/">Volver</a>')
        
        
        elif solicitud == 'morosos':
            return HttpResponseRedirect(urlbase+"morosos")
        elif solicitud == 'futuros_morosos':
            return HttpResponseRedirect(urlbase+"futuros_morosos")
        elif solicitud == 'prestamo_fecha':
            formPrestamo_fecha=Prestamo_fechaForm(request.GET)
            if formPrestamo_fecha.is_valid():
                fecha=formPrestamo_fecha.cleaned_data['Fecha']
                #print(type(fecha))
                #fecha = str(fecha.Fecha)
                return redirect(urlbase+"prestamo_fecha/" + str(fecha))
            else:
                return HttpResponse('Fecha no valida... El formato debe ser YYYY-MM-DD. <br><a href="/biblio/">Volver</a>')

    
    #default
    formSocio = SocioForm()
    formLibro = LibroForm()
    formMorosos = MorososForm()
    formFuturos_morosos = Futuros_morososForm()
    formPrestamo_fecha = Prestamo_fechaForm()
    formCopia = CopiaForm()
    formPrestamo = PrestamoForm()
    formDevolucion = DevolucionForm()
    formAltaSocio = AltaSocioForm()
    formAltaLibro = AltaLibroForm()

    template = loader.get_template('biblio/index.html')
    context = {
        'formSocio': formSocio,
        'formLibro': formLibro,
        'formMorosos': formMorosos,
        'formFuturos_morosos': formFuturos_morosos,
        'formPrestamo_fecha': formPrestamo_fecha,
        'formCopia': formCopia,
        'formPrestamo': formPrestamo,
        'formDevolucion': formDevolucion,
        'formAltaSocio':formAltaSocio,
        'formAltaLibro': formAltaLibro,
    }
    #print(template.render(context, request))
    return render(request,'biblio/index.html',context)


def prestamo(request,Id_socio,Isbn):

    try:
        socio = GestorSocios.get(Id_socio=Id_socio)
    except Exception as e:
        if type(e).__name__ == 'DoesNotExist':
            return HttpResponse("El Socio no existe " + Id_socio +"<br><a href='/biblio/'>Volver</a>")
        else:
            return HttpResponse(type(e).__name__)

    if socio.Estado_moroso:
        return HttpResponse("El Socio " + Id_socio + " es moroso. <br><a href='/biblio/'>Volver</a>")

    copia = GestorCopias.getCopiaDisponible(Isbn)

    if copia == "No hay copias disponibles":
        return HttpResponse("No hay copias disponibles para " + Isbn + "<br><a href='/biblio/'>Volver</a>")

    prestamo = Prestamo(Inventario = copia, Id_socio = socio, Fecha_prestamo = str(time.strftime("%Y-%m-%d")))
    prestamo.save()

    #print(prestamo)

    return HttpResponse("Se prestó una copia del libro " + Isbn + " al socio "+ Id_socio +"<br><a href='/biblio/'>Volver</a>")


def devolucion(request,Id_socio,Inventario):
    resultadoDevolucion = GestorPrestamos.devolver(Id_socio,Inventario)
    return HttpResponse(str(resultadoDevolucion))


def info_socio(request,Id_socio):
    socio_inst = get_object_or_404(Socio, pk=Id_socio)
    prestamo_lista = GestorPrestamos.getPrestados(Id_socio = Id_socio)

    template = loader.get_template('biblio/info_socio.html')
    context = {
        'socio': socio_inst,
        'prestamo_lista': prestamo_lista,
    }
    return HttpResponse(template.render(context, request))


def info_copia(request,Inventario):
    copia_inst = get_object_or_404(Copia, pk = Inventario)
    if copia_inst.Prestado == False:
        template = loader.get_template('biblio/info_copia.html')
        context = {
            'copia': copia_inst,
        }
        return HttpResponse(template.render(context, request))

    prestamo_inst = GestorPrestamos.getPrestados(Inventario = Inventario, Estado = 'Pendiente')[0]
    socio_inst = prestamo_inst.Id_socio
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
    lista_prestamos_atrasados = list(filter(lambda futuro_moroso: futuro_moroso.estaDemorado(), lista_pendientes))


    lista_futuros_morosos = []
    [lista_futuros_morosos.append(prestamo.Id_socio) for prestamo in lista_prestamos_atrasados if prestamo.Id_socio not in lista_futuros_morosos]

    template = loader.get_template('biblio/futuros_morosos.html')
    context = {
        'lista_futuros_morosos': lista_futuros_morosos,
    }
    return HttpResponse(template.render(context, request))


def prestamo_fecha(request,fecha):
    try:
        fechaValidada = datetime.datetime.strptime(fecha, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Formato de fecha incorrecto, debe ser YYYY-MM-DD")

    #lista=[str(i) for i in GestorPrestamos.getPrestados(Fecha_prestamo=fecha)]
    lista=[{'Inventario': i.Inventario,
            'Fecha_prestamo': str(i.Fecha_prestamo),
            'Fecha_devolucion': str(i.Calcular_Fecha_devolucion()),
            'Estado': i.Estado,
            } for i in GestorPrestamos.getPrestados(Fecha_prestamo=fecha)]
    #Calcular_Fecha_devolucion()

    template = loader.get_template('biblio/prestamo_fecha.html')
    context = {
        'fecha': fecha,
        'listaPrestamo': lista,
    }
    return HttpResponse(template.render(context, request))
