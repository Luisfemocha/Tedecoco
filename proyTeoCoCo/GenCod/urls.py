from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('inicio',views.inicio,name='inicio'),
    path('conceptos',views.conceptos,name='conceptos'),
    path('notas',views.notas,name='notas'),
    path('conexiones',views.conexiones,name='conexiones'),
    path('comprobar',views.comprobar,name='comprobar'),
    path('identificar',views.identificar,name='identificar'),
    path('formularioCreado',views.formularioCreado,name='formularioCreado'),
    path('tablaCreada',views.tablaCreada,name='tablaCreada'),
    path('modificar',views.modificar,name='modificar'),
    path('crear',views.crear,name='crear'),
    path('eliminar',views.eliminar,name='eliminar'),
    path('editar',views.editar,name='editar'),
]