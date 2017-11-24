from django.conf.urls import url
from . import views
#url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
app_name = 'biblio'
urlpatterns= [
    url(r'^$', views.index, name='index'),
    url(r'^socio/(?P<Id_socio>[1-9][0-9]*)/$', views.info_socio, name='info_socio'),
    url(r'^copia/(?P<Inventario>[1-9][0-9]*)/$', views.info_copia, name='info_copia'),
    url(r'^libro/(?P<Isbn>[1-9][0-9]{12,12})/$', views.info_libro, name='info_libro'),
    url(r'^morosos/$', views.morosos, name='morosos'),
    url(r'^futuros_morosos/$', views.futuros_morosos, name='futuros_morosos'),
    url(r'^prestamo_fecha/(?P<fecha>[0-9a-zA-Z\-\/]+)/$', views.prestamo_fecha, name='prestamo_fecha'),
    url(r'^prestamo/(?P<Id_socio>[1-9][0-9]*)/(?P<Isbn>[1-9][0-9]{12,12})/$', views.prestamo, name='info_prestamo'),
    url(r'^devolucion/(?P<Id_socio>[1-9][0-9]*)/(?P<Inventario>[1-9][0-9]*)/$', views.devolucion, name='info_devolucion'),
    url(r'^.*$', views.index, name='default'),
    ]
    
#prueba update