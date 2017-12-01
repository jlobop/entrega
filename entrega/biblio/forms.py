from django import forms
from .models import *

'''
class SocioForm(forms.ModelForm):
    class Meta:
        model=Socio
        #fields=('Id_socio',)
        fields='__all__'

class LibroForm(forms.ModelForm):
    class Meta:
        model=Libro
        fields=('Isbn',)
'''

class SocioForm(forms.Form):
    #Id_socio = forms.IntegerField()
    Id_socio = forms.ModelChoiceField(queryset=Socio.objects.all())
    solicitud = forms.CharField( widget=forms.HiddenInput(),initial='info_socio')

class LibroForm(forms.Form):
    Isbn = forms.ModelChoiceField(queryset=Libro.objects.all())
    solicitud = forms.CharField( widget=forms.HiddenInput(),initial='info_libro')


class AltaSocioForm(forms.Form):
    #Id_socio = forms.IntegerField()
    solicitud = forms.CharField( widget=forms.HiddenInput(),initial='alta_socio')   
    Nombre = forms.CharField(max_length=20)
    Apellido = forms.CharField(max_length=20)
    Email = forms.EmailField()
    Fecha_nac = forms.DateField(widget=forms.widgets.DateInput(format="%Y-%m-%d"),label='Fecha de Nacimiento')

class AltaLibroForm(forms.Form):   
    solicitud = forms.CharField( widget=forms.HiddenInput(),initial='alta_libro')   
    Isbn = forms.IntegerField(min_value=1000000000000,max_value=9999999999999)
    Titulo = forms.CharField(max_length=60)
    Autor = forms.CharField(max_length=60)
    Fecha_ingreso = forms.DateField(widget=forms.widgets.DateInput(format="%Y-%m-%d"),initial=datetime.date.today())
    ncopias = forms.IntegerField(min_value=1,max_value=10,initial=1,label='Cantidad de Copias')

class CopiaForm(forms.Form):
    Inventario = forms.ModelChoiceField(queryset=Copia.objects.all())
    solicitud = forms.CharField( widget=forms.HiddenInput(),initial='info_copia')
    
class MorososForm(forms.Form):
    solicitud = forms.CharField( widget=forms.HiddenInput(),initial='morosos')

class Futuros_morososForm(forms.Form):
    solicitud = forms.CharField( widget=forms.HiddenInput(),initial='futuros_morosos')

class Prestamo_fechaForm(forms.Form):
    Fecha=forms.DateField(widget=forms.widgets.DateInput(format="%Y-%m-%d"))
    solicitud = forms.CharField( widget=forms.HiddenInput(),initial='prestamo_fecha')
    
class PrestamoForm(forms.Form):
    Id_socio = forms.ModelChoiceField(queryset=Socio.objects.filter(Estado_moroso=False),label='Socio (no moroso)')
    Isbn = forms.ModelChoiceField(queryset=Libro.objects.all())
    solicitud = forms.CharField( widget=forms.HiddenInput(),initial='prestamo')
    
class DevolucionForm(forms.Form):
    Id_socio = forms.ModelChoiceField(queryset=Socio.objects.all())
    Inventario = forms.ModelChoiceField(queryset=Copia.objects.filter(Prestado=True))
    solicitud = forms.CharField( widget=forms.HiddenInput(),initial='devolucion')