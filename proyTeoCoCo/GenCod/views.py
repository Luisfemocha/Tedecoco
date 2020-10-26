from django.shortcuts import render
from django.http import HttpResponse
import zlib
import io
import base64
import xmltodict
import pprint
import json
import urllib.parse
from urllib.parse import unquote
import xml.etree.ElementTree as ET
import re
from xml.dom import minidom
import codecs
import ast 
from .funciones import *

def index(request):
    return render(request,"index.html")

def inicio(request):
    Aux=request.POST['contenidoJson']
    Aux=Aux.replace("\'", "\"")
    A=json.loads(Aux)
    lista=[]
    return render(request, "listaObjetos.html", {'jsonList': A})

def conceptos(request):
    Aux=request.POST['contenidoJson']
    Aux=Aux.replace("\'", "\"")
    A=json.loads(Aux)
    lista=[]
    for i in range(2, len(A)):
        if "rounded=0" in A[i]['@style'] and "dashed=1" not in A[i]['@style'] and "edgeStyle=orthogonalEdgeStyle" not in A[i]['@style'] and "@value" in A[i] and A[i]['@value'] != "":
            lista.append(A[i]["@value"])
    return render(request,"listaConceptos.html",{'listaConceptos':lista})


def notas(request):
    Aux=request.POST['contenidoJson']
    Aux=Aux.replace("\'", "\"")
    A=json.loads(Aux)
    lista=[]
    for i in range(2, len(A)):
        if "rounded=0" in A[i]['@style'] and "dashed=1" in A[i]['@style'] and "edgeStyle=orthogonalEdgeStyle" not in A[i]['@style'] and "@value" in A[i]:
            lista.append(A[i]["@value"])
    return render(request,"listaNotas.html",{'listaConceptos':lista})

def conexiones(request):
    Aux=request.POST['contenidoJson']
    Aux=Aux.replace("\'", "\"")
    A=json.loads(Aux)
    lista=[] #tupla id,desde, hasta
    flechas=[]
    def dato(id,A):
        for i in range(2, len(A)):
            if id == A[i]["@id"]:
                return A[i]["@value"]
    
    for i in range(2, len(A)):
        if "edgeStyle=orthogonalEdgeStyle" in A[i]['@style']:
          lista.append((A[i]["@source"],dato(A[i]["@source"],A),dato(A[i]["@target"],A)))
    return render(request,"listaConexiones.html",{'listaConceptos':lista})

def comprobar(request):
    Aux=request.POST['contenidoJson']
    Aux=Aux.replace("\'", "\"")
    A=json.loads(Aux)
    return render(request,"comprobar.html")

def identificar(request):
    nombre=request.FILES['archivoXml']
    tree = ET.parse(nombre) #Se elige el archivo 
    root = tree.getroot()
    decoded_data = base64.b64decode(root[0].text)
    res=zlib.decompress(decoded_data , -15)
    aux=str(res)
    final=unquote(aux)
    final=final[2:len(final)-1] #Formato XML
    fin=json.dumps(xmltodict.parse(final))
    inicio=json.loads(fin)
    json_pretty = json.dumps(inicio, sort_keys=True, indent=4)
    objetos=inicio['mxGraphModel']['root']['mxCell']
    if(revisarDiagrama(objetos)):
        vistas,forms=generarHTML(objetos)
        triadas=triadaEstructural(objetos)
        mensajes=htmlFormulario(triadas,vistas,forms)
        contenido=generarHtmlFormulario(mensajes,vistas)
        botones,tipos_datos, nombres_atr=datosTabla(triadas)
        mensajes2=htmlTabla(nombres_atr)
        generarHtmlTabla(mensajes2) 
        return render(request,"identificar.html",{'mensaje1':"Existe un formulario",'jsonList': objetos,'datos':nombres_atr})
    else:
        return render(request,"identificar.html",{'mensaje2':"No Hay formulario",'jsonList': objetos})


def formularioCreado(request):
    datos=request.POST['datos']
    res=ast.literal_eval(datos) 
    pwd = os.path.dirname(__file__)
    return render(request,pwd +'\\templates\\generados\\formulario.html',{'datos':res})

def tablaCreada(request):
    pwd = os.path.dirname(__file__)
    return render(request,pwd +'\\templates\\generados\\tabla.html')

def modificar(request):
    return HttpResponse("Falta eso")

def crear(request):
    pwd = os.path.dirname(__file__)
    datosForm=[]
    datos=request.GET['datos']
    objeto={}
    res=ast.literal_eval(datos)
    for x in res:
        datosForm.append(request.GET[x])
    for i in range(len(datosForm)):
        objeto[res[i]]=datosForm[i]
    json_data = json.dumps(objeto)
    tamaño=len(res)
    return render(request,pwd +'\\templates\\generados\\tabla.html',{'objetos':datosForm,'rango':tamaño})