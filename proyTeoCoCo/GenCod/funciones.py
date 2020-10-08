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
import functools
import operator
import os




def dato(id,A):
    for i in range(2, len(A)):
        if id in A[i]["@id"]:
            return A[i]["@value"]



def flecha(A):
    flechas=[]
    for i in range(2, len(A)):
        if "edgeStyle=orthogonalEdgeStyle" in A[i]['@style']:
          flechas.append(A[i])
          #print ("La flecha va desde: ", dato(A[i]["@source"], A), " Hasta: ", dato(A[i]["@target"], A))
    return flechas


def triadaFormulario(A):
  listaFlechas= flecha(A) # Se encuentran todas las flechas
  desdeHasta=[] # lista de tuplas de la forma (idDesde,desde,hasta)
  boolean=False
  for fle in listaFlechas:
    desdeHasta.append((fle["@source"],dato(fle["@source"], A),dato(fle["@target"], A))) #Se agrega a la lista, la tupla 
  try:
    #Se verifica la correcta conexión de las flechas
    for i in range(len(desdeHasta)):
      ###### REGEX DESDE
      regexFormulario1 = re.match(r"(\bFORM\b) (?<!\S)\w+(?!\S)", desdeHasta[i][1])
      regexBoton1= re.match(r"(\bBOTON\b) (?<!\S)\w+(?!\S)", desdeHasta[i][1])
      regexVista1= re.match(r"(\bVISTA\b) (?<!\S)\w+(?!\S)", desdeHasta[i][1])
      regexVistas1= re.match(r"(\bVISTAS\b)", desdeHasta[i][1])
      regexTiene1=re.match(r"(\btiene\b)", desdeHasta[i][1])
      ######### REGEX HASTA
      regexFormulario2 = re.match(r"(\bFORM\b) (?<!\S)\w+(?!\S)", desdeHasta[i][2])
      regexBoton2= re.match(r"(\bBOTON\b) (?<!\S)\w+(?!\S)", desdeHasta[i][2])
      regexVista2= re.match(r"(\bVISTA\b) (?<!\S)\w+(?!\S)", desdeHasta[i][2])
      regexVistas2= re.match(r"(\bVISTAS\b)", desdeHasta[i][2])
      regexTiene2=re.match(r"(\btiene\b)", desdeHasta[i][2])
      if regexTiene1:
        lis=[(id,desde,hasta) for id, desde,hasta in desdeHasta if id  == desdeHasta[i][0] ]
        if len(lis)==3: #Identifica el "tiene" que se divide en 3
          if regexFormulario2:
            print("tiene hasta FORM correcto")
            boolean=True
          elif regexBoton2:
            print("tiene hasta BOTON correcto")
            boolean=True
          else:
            print("Incorrecto")
            boolean=False
        else:
          print("tiene hasta atributos correcto")
          boolean=True#elif # Debe revisar que si sea una nota los atributos de formulario, [FALTA ESO]
      elif regexVistas1 and regexVista2:
        boolean=True
        print("Vistas a vista correcto")
      elif regexVista1 and regexTiene2:
        boolean=True
        print("vista a tiene correcto")
      elif regexBoton1 and 'click' in desdeHasta[i][2]:
        print("boton a click correcto")
        boolean=True
      elif regexFormulario1 and regexTiene2:
        print("formulario hasta tiene correcto")
        boolean=True
      else:
        boolean=False
        break
      
    if boolean ==True:
      return True
      #print("Sintaxis válida, se manda a crear el HTML de formulario")
    else:
      raise Exception
  except:
      return False
    #print("No es correcta la sintaxis")
  return (desdeHasta)

def triadaEstructural( A):
  listaFlechas= flecha(A) # Se encuentran todas las flechas
  desdeHasta=[] # lista de tuplas de la forma (idDesde,desde,hasta)
  desde=[]
  for fle in listaFlechas:
    desde.append(((fle["@source"]),dato(fle["@source"], A),(fle["@target"]))) 
  
  for fle in listaFlechas:
    desdeHasta.append(((fle["@source"]),dato(fle["@source"], A),dato(fle["@target"], A))) 
  print(" ")
  final=[desdeHasta[x] for x in range(len(desdeHasta)) if desdeHasta[x][1]=='tiene']
  
  relacion=[]
  for i in range(len(final)):
    for j in range(len(desde)):
      if(final[i][0]== desde[j][2]):        
        relacion.append((desde[j][1],  dato(final[i][0], A) ,(final[i][2]) ))   

  return  relacion



def generarHTML(A):
    conceptos=[]
    relacion=triadaEstructural(A)
    for i in range(2, len(A)):
        if "rounded=0" in A[i]['@style'] and "dashed=1" not in A[i]['@style'] and "edgeStyle=orthogonalEdgeStyle" not in A[i]['@style'] and "@value" in A[i] and A[i]['@value'] != "":
            conceptos.append(A[i]["@value"])
    vistas=[conceptos[i] for i in range(len(conceptos)) if  re.match(r"(\bVISTA\b) (?<!\S)\w+(?!\S)", conceptos[i])]
    forms= [conceptos[i] for i in range(len(conceptos)) if  re.match(r"(\bFORM\b) (?<!\S)\w+(?!\S)", conceptos[i])]
    for k in range(len(vistas)):
      print("Se debe hacer ", vistas[k])
    print("En total se deben hacer ",len(vistas ), " vista(s)")

    return vistas,forms


def atributos(triadas, forms):
  for triada in triadas: 
    for form in forms: 
      if(form==triada[0]):
        atr=(triada[2])
        
      
  atributos=re.split(r';',atr)
  atributos.pop()
  atrib=[re.split(r':',x)for x in atributos]
  #print(atrib)

  k='<br>*atributo1'
  def arreglar(k):
    j=re.split(r'[<br>]*[*]',k)
    j.pop(0)
    return j
  tipos_datos=[atrib[i][1]for i in range(len(atrib))]
  nombres_atr=[arreglar(atrib[i][0]) for i in range(len(atrib))]
  #print(tipos_datos)
  nombres_atr=functools.reduce(operator.iconcat, nombres_atr, [])
  #print(nombres_atr)
  return (tipos_datos, nombres_atr)


def htmlFormulario(triadas,vistas,forms):

  mensajes=[]
  for triada in triadas:

    for vista in vistas:
      
      if(triada[0]==vista):      
        if(re.match(r"(\bFORM\b) (?<!\S)\w+(?!\S)", triada[2])):
          nombre_form=triada[2]
          nombre_form=nombre_form.replace('FORM ', '') 
          tipos_datos, nombres_atr= atributos(triadas, forms)     
          mensajes.append((vistas.index(vista),"<form action="+"\""+"mmmm"+"\""+" metod="+"\""+"post"+"\""+" id="+"\""+nombre_form+"\" "+"nombre="+"\""+nombre_form+"\" "+">"))
          for i in range(len(tipos_datos)):
            mensajes.append((vistas.index(vista),nombres_atr[i]+":<br>"))
            
            mensajes.append((vistas.index(vista),"<input type="+"\""+tipos_datos[i]+"\""+" name="+"\""+nombres_atr[i]+"\""+" id="+"\""+nombres_atr[i]+"\""+"class='form-control' ><br>"))
          mensajes.append((vistas.index(vista),"</form>"))
        elif(re.match(r"(\bBOTON\b) (?<!\S)\w+(?!\S)", triada[2])):
          result = re.match(r'\S*\s(\S*)', triada[2])
          p=result.group(1)

          mensajes.append((vistas.index(vista),("<button name="+"\""+p+"\""+">"+p+"</button>")))
  return mensajes


def generarHtmlFormulario(mensajes,vistas):
  pwd = os.path.dirname(__file__)
  print(pwd)
  contenido=''
  for k in range(len(mensajes)):
    for j in range (len(vistas)):
      
      if mensajes[k][0]==j:
        contenido += mensajes[k][1] + '\n'

  for i in range(len(vistas)):
    f=open(pwd + '\\templates\\generados\\formulario.html','wt')
    
    mensaje = """
    {% extends 'base.html' %}
    {% block content %}
    <html>
    <div class="container">
    <head>"""+vistas[i]+"""</head>
    <body><p> Ensayo primer formulario</p>
    
        """+contenido+""" 
    </div>
    </body>
    </html>
    {% endblock %}
    """
    f.write(mensaje)
    f.close()
  return contenido