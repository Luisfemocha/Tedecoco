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
        if id == A[i]["@id"]:
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
  final=[desdeHasta[x] for x in range(len(desdeHasta)) if desdeHasta[x][1]=='tiene' or desdeHasta[x][1]=='CONTENIDO']
  
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
  tipos_datos=[atrib[i][1]for i in range(len(atrib))]
  for i in range(len(tipos_datos)):
    tipos_datos[i]=tipos_datos[i].replace(" ","")
  nombres_atr=[arreglar(atrib[i][0]) for i in range(len(atrib))]
  #print(tipos_datos)
  nombres_atr=functools.reduce(operator.iconcat, nombres_atr, [])
  #print(nombres_atr)
  return (tipos_datos, nombres_atr)


def arreglar(k):
    j=re.split(r'[<br>]*[*]',k)
    j.pop(0)
    return j

def htmlFormulario(triadas,vistas,forms):
  mensajes=[]
  for triada in triadas:

    for vista in vistas:
      if(re.match(r"(\bFORM\b) (?<!\S)\w+(?!\S)", triada[2]) and re.match(r"(\bVISTA\b) (\bhome\b)", vista)):
          nombre_form=triada[2]
          nombre_form=nombre_form.replace('FORM ', '') 
          tipos_datos, nombres_atr= atributos(triadas, forms)     
          mensajes.append((vistas.index(vista),"<form action="+"\""+"crear"+"\""+" metod="+"\""+"post"+"\""+" id="+"\""+nombre_form+"\" "+"nombre="+"\""+nombre_form+"\" "+">"))
          for i in range(len(tipos_datos)):
            mensajes.append((vistas.index(vista),"<div class='form-group'>"))
            mensajes.append((vistas.index(vista),"<label for="+nombres_atr[i]+"class ='control-label'>"+nombres_atr[i]+"</label>"))
            mensajes.append((vistas.index(vista),"<input type="+"\""+tipos_datos[i]+"\""+" name="+"\""+nombres_atr[i]+"\""+" id="+"\""+nombres_atr[i]+"\""+"class='form-control'><br>"))
            mensajes.append((vistas.index(vista),"</div>"))
          mensajes.append((vistas.index(vista),"<input type='hidden' class='form-control form-control-lg' value='{{datos}}' name='datos'>"))
          mensajes.append((vistas.index(vista),"<input type='hidden' class='form-control form-control-lg' value='{{listaObjetos}}' name='listaObjetos'>"))
  for vista in vistas:
    if(re.match(r"(\bVISTA\b) (\bhome\b)", vista)):
      for triada in triadas:
        if(re.match(r"(\bBOTON\b) (?<!\S)\w+(?!\S)", triada[2] )and re.match(r"(\bVISTA\b) (\bhome\b)", triada[0])):
          result = re.match(r'\S*\s(\S*)', triada[2])
          p=result.group(1)
          if p == "guardar":
            mensajes.append((vistas.index(vista),("<button type='submit' class='btn btn-success'>"+p+"</button>")))
            mensajes.append((vistas.index(vista),"</form>"))
          else:
            mensajes.append((vistas.index(vista),("<form method='POST' action='tablaCreada' enctype='multipart/form-data'>{% csrf_token %}<input type='hidden' class='form-control form-control-lg' value='{{datos}}' name='datos'><input type='hidden' class='form-control form-control-lg' value='{{listaObjetos}}' name='listaObjetos'><button type='submit' class='btn btn-info btn-lg btn-primary'>"+p+"</button></form>")))
  return mensajes


def generarHtmlFormulario(mensajes,vistas):
  pwd = os.path.dirname(__file__)
  contenido=''
  for k in range(len(mensajes)):
    for j in range (len(vistas)):
      
      if mensajes[k][0]==j:
        contenido += mensajes[k][1] + '\n'

  for i in range(len(vistas)):
    if(re.match(r"(\bVISTA\b) (\bhome\b)", vistas[i])):
      f=open(pwd + '\\templates\\generados\\formulario.html','wt')
      
      mensaje = """
          {% extends 'base.html' %}
          {% block content %}
          <html>

          <div class="container">
          <h3>"""+vistas[i]+"""</h3>
              """+contenido+""" 
          </div>
          </body>
          </html>
          {% endblock %}
          """
      f.write(mensaje)
      f.close()
  return contenido

def concepto(A):
    listaConceptos=[]
    for i in range(2, len(A)):
        if "rounded=0" in A[i]['@style'] and "dashed=1" not in A[i]['@style'] and "edgeStyle=orthogonalEdgeStyle" not in A[i]['@style'] and "@value" in A[i] and A[i]['@value'] != "":
            listaConceptos.append(A[i]["@value"])
            #print ("Es un concepto que dice: ", A[i]["@value"])
    return listaConceptos

def revisarDiagrama(A):
  desdeHasta=[]
  listaFlechas= flecha(A)
  conp=revisarConceptos(A)
  if conp==False:
    return False
  res=False
  for fle in listaFlechas:
    desdeHasta.append((dato(fle["@source"], A),dato(fle["@target"], A)))
  for i in range(len(desdeHasta)):
    #DESDE
    formulario = re.match(r"(\bFORM\b) (?<!\S)\w+(?!\S)", desdeHasta[i][0])
    boton = re.match(r"(\bBOTON\b) (?<!\S)\w+(?!\S)", desdeHasta[i][0])
    vista = re.match(r"(\bVISTA\b) (?<!\S)\w+(?!\S)", desdeHasta[i][0])
    contenido = re.match(r"(\bCONTENIDO\b)", desdeHasta[i][0])
    tabla = re.match(r"(\bTABLA\b)", desdeHasta[i][0])
    vistas = re.match(r"(\bVISTAS\b)", desdeHasta[i][0])
    tiene = re.match(r"(\btiene\b)", desdeHasta[i][0])
    if vistas:
      vista2 = re.match(r"(\bVISTA\b) (?<!\S)\w+(?!\S)", desdeHasta[i][1])
      if vista2:
        res=True
      else:
        return "No es correcta la sintaxis, error en VISTA"
    elif boton:
      vista2 = re.match(r"(\bVISTA\b) (?<!\S)\w+(?!\S)", desdeHasta[i][1])
      if vista2:
        res=True
      else:
        return "No es correcta la sintaxis, error en BOTON a vista"
    elif vista:
      tiene2 = re.match(r"(\btiene\b)", desdeHasta[i][1])
      if tiene2:
        res=True
      else:
        return "No es correcta la sintaxis, error en VISTA a tiene"
    elif formulario:
      tiene2 = re.match(r"(\btiene\b)", desdeHasta[i][1])
      if tiene2:
        res=True
      else:
        return "No es correcta la sintaxis, error en FORM a tiene"
    elif tiene:
      formulario2 = re.match(r"(\bFORM\b) (?<!\S)\w+(?!\S)", desdeHasta[i][1])
      boton2 = re.match(r"(\bBOTON\b) (?<!\S)\w+(?!\S)", desdeHasta[i][1])
      contenido2 = re.match(r"(\bCONTENIDO\b)", desdeHasta[i][1])
      tabla2 = re.match(r"(\bTABLA\b)", desdeHasta[i][1])
      nota=re.match(r"(^'*.*;$)", desdeHasta[i][1])
      if formulario2 or boton2 or contenido2 or tabla2:
        res=True
      elif nota:
        res=True
      else:
        return "No es correcta la sintaxis de algún tiene"
    elif tabla:
      tiene2 = re.match(r"(\btiene\b)", desdeHasta[i][1])
      if tiene2:
        res=True
      else:
        return "No es correcta la sintaxis, error en FORM a tiene"
    elif contenido:
      nota=re.match(r"(^'*.*;$)", desdeHasta[i][1])
      if nota:
        res=True
      else:
        return "No es correcta la sintaxis de contenido hacia Atributos"
    else:
      return False

  if res:
    print("Es correcta la sintaxis, se manda a crear todo")
  return res




def revisarConceptos(A):
  listaConceptos=[]
  listaConceptos= concepto(A)
  print(listaConceptos)
  res=True
  for i in range(len(listaConceptos)):
    formulario = re.match(r"(\bFORM\b) (?<!\S)\w+(?!\S)", listaConceptos[i])
    boton = re.match(r"(\bBOTON\b) (?<!\S)\w+(?!\S)", listaConceptos[i])
    vista = re.match(r"(\bVISTA\b) (?<!\S)\w+(?!\S)", listaConceptos[i])
    contenido = re.match(r"(\bCONTENIDO\b)", listaConceptos[i])
    tabla = re.match(r"(\bTABLA\b)", listaConceptos[i])
    if formulario or boton or vista or contenido or tabla:
      res=True
    else:
      return False
  return res

def datosTabla(triadas):
  botones=[]
  atributos=[]
  atr=""
  for triada in triadas:
    vista = re.match(r"(\bVISTA\b) (\bleer\b)", triada[0])
    tiene = re.match(r"(\btiene\b)", triada[0])
    if vista:
      boton = re.match(r"(\bBOTON\b) (?<!\S)\w+(?!\S)", triada[2])
      if boton:
        botones.append(triada[2][6:])
    elif tiene:
      atr=(triada[2])

  atributos=re.split(r';',atr)
  atributos.pop()
  atrib=[re.split(r':',x)for x in atributos]
  tipos_datos=[atrib[i][1]for i in range(len(atrib))]
  for i in range(len(tipos_datos)):
    tipos_datos[i]=tipos_datos[i].replace(" ","")
  nombres_atr=[arreglar(atrib[i][0]) for i in range(len(atrib))]
  nombres_atr=functools.reduce(operator.iconcat, nombres_atr, []) 

  return botones,tipos_datos, nombres_atr


def datosModificar(triadas):
  botones=[]
  for triada in triadas:
    vista = re.match(r"(\bVISTA\b) (\bmodificar\b)", triada[0])
    if vista:
      boton = re.match(r"(\bBOTON\b) (?<!\S)\w+(?!\S)", triada[2])
      if boton:
        botones.append(triada[2][6:])
  return botones

def htmlTabla(nombres_atributos):
  mensajes=[]
  for i in range(len(nombres_atributos)):
    mensajes.append("<th scope='col'>"+nombres_atributos[i]+"</th>")
  return mensajes

def generarHtmlTabla(mensajes):
  pwd = os.path.dirname(__file__)
  contenido=""
  for i in range(len(mensajes)):
    contenido +=mensajes[i] + '\n'
  f=open(pwd + '\\templates\\generados\\tabla.html','wt')
  mensaje = """
          {% extends 'base.html' %}
          {% block content %}
          <html>
          <body>
          <div class="container">
          <h1>VISTA leer</h1>
          <table class="table">
          <thead>
          <tr> 
              """+contenido+"""
              <th scope='col'> </th>
              <th scope='col'> </th>
          </tr> 
          </thead>
          <tbody>  
          {%if listaObjetos|length > 0 %}
          {%for obj in listaObjetos %}
          <tr>
          {%for cont in obj %}
          <td>{{cont}}</td>         
          {%endfor%}
          <td>
           <form method="POST" action="modificar" enctype="multipart/form-data">
              {% csrf_token %}
              <input type='hidden' class='form-control form-control-lg' value='{{datos}}' name='datos'>
              <input type="hidden" class="form-control form-control-lg" value="{{listaObjetos}}" name="listaObjetos">
              <input type="hidden" class="form-control form-control-lg" value="{{obj}}" name="objeto">
              <button type="submit" class="btn btn-warning btn-lg btn-primary">modificar</button>
            </form>
          </td>
          <td>
           <form method="POST" action="eliminar" enctype="multipart/form-data">
              {% csrf_token %}
              <input type='hidden' class='form-control form-control-lg' value='{{datos}}' name='datos'>
              <input type="hidden" class="form-control form-control-lg" value="{{listaObjetos}}" name="listaObjetos">
              <input type="hidden" class="form-control form-control-lg" value="{{obj}}" name="objeto">
              <button type="submit" class="btn btn-danger btn-lg btn-primary">eliminar</button>
            </form>
          </td>
          </tr>
          {%endfor%}
          {%endif%}
          </tbody> 
          </table>
          <form method="POST" action="formularioCreado" enctype="multipart/form-data">
              {% csrf_token %}
              <input type='hidden' class='form-control form-control-lg' value='{{datos}}' name='datos'>
              <input type="hidden" class="form-control form-control-lg" value="{{listaObjetos}}" name="listaObjetos">
              <button type="submit" class="btn btn-info btn-lg btn-primary">volver</button>
            </form>
          </div>
          </body>
          </html>
          {% endblock %}
          """
  f.write(mensaje)
  f.close()


def htmlModificar(datos,objeto):
  mensajes=[]
  mensajes.append("<form action="+"\""+"editar"+"\""+" metod="+"\""+"post"+"\">")
  for x in range(len(datos)):
    mensajes.append("<div class='form-group'>")
    mensajes.append("<label for="+datos[x]+"class ='control-label'>"+datos[x]+"</label>")
    mensajes.append("<input type="+"\""+datos[x]+"\""+" name="+"\""+datos[x]+"\""+" id="+"\""+datos[x]+"\""+"value='"+objeto[x]+"' class='form-control' placeholder="+objeto[x]+"><br>")
    mensajes.append("</div>")
  mensajes.append("<input type='hidden' class='form-control form-control-lg' value='{{datos}}' name='datos'>")
  mensajes.append("<input type='hidden' class='form-control form-control-lg' value='{{listaObjetos}}' name='listaObjetos'>")
  mensajes.append("<input type='hidden' class='form-control form-control-lg' value='{{objeto}}' name='objeto'>")
  mensajes.append("<button type='submit' class='btn btn-warning'>modificar</button>")
  mensajes.append("</form>")
  return mensajes

def crearModificar(mensajes):
  pwd = os.path.dirname(__file__)
  contenido=""
  for i in range(len(mensajes)):
    contenido += mensajes[i] + '\n'
  f=open(pwd + '\\templates\\generados\\modificar.html','wt')
  mensaje = """
          {% extends 'base.html' %}
          {% block content %}
          <html>
          <div class="container">
          <head>"""+"modificar"+"""</head>
              """+contenido+""" 
          </div>
          </body>
          </html>
          {% endblock %}
          """
  f.write(mensaje)
  f.close()