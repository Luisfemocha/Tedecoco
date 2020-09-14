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