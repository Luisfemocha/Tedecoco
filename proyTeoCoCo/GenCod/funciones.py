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