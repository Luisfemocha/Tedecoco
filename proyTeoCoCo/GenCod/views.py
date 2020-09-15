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

def index(request):
    return render(request,"index.html")

def inicio(request):
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
    #return HttpResponse(json.dumps(inicio['mxGraphModel']['root']['mxCell'],indent=4))
    return render(request, "listaObjetos.html", {'jsonList': inicio['mxGraphModel']['root']['mxCell']})

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
            if id in A[i]["@id"]:
                return A[i]["@value"]
    
    for i in range(2, len(A)):
        if "edgeStyle=orthogonalEdgeStyle" in A[i]['@style']:
          lista.append((A[i]["@source"],dato(A[i]["@source"],A),dato(A[i]["@target"],A)))
    return render(request,"listaConexiones.html",{'listaConceptos':lista})

