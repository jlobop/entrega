from django import forms
from .models import *

class SocioForm(forms.ModelForm):
    class Meta:
        model=Socio
        fields=('Apellido','Id','Nombre')


class LibroForm(forms.ModelForm):
    class Meta:
        model=Libro
        fields=('Isbn',)
