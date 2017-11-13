from django.contrib import admin

# Register your models here.
from .models import Libro
admin.site.register(Libro)

from .models import Prestamo
admin.site.register(Prestamo)

from .models import Copia
admin.site.register(Copia)

from .models import Socio
admin.site.register(Socio)