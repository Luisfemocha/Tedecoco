from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('inicio',views.inicio,name='inicio'),
    path('conceptos',views.conceptos,name='conceptos'),
    path('notas',views.notas,name='notas'),
    path('conexiones',views.conexiones,name='conexiones'),
    #path('comprobar',views.comprobar,name='comprobar'),
]