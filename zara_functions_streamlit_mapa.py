import streamlit as st
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim 
import folium


#datos: nuestro dataset
#columna: la columna sobre la que queremos filtrar la búsqueda
#key: la clave del input correspondiente

datos = pd.read_csv('datos_zara_procesados.csv')

def quitar_acentos(palabra):
    acentos = ['Á', 'É', 'Í', 'Ó', 'Ú']
    no_acentos = ['A', 'E', 'I', 'O', 'U']
    for letra in palabra:
        if letra in acentos:
            posc = acentos.index(letra)
            palabra = palabra.replace(letra, no_acentos[posc])
    return palabra 

def buscador_prenda_mapa(datos,key):
    prenda = key.upper()
    prenda = quitar_acentos(prenda)
    prenda_selec = datos['nombre_prenda'][datos['nombre_prenda'] == prenda].unique()
    prenda_selec = list(prenda_selec)
    return prenda_selec

#Nos creamos un dataframe que tenga solo las direcciones que contengan las tallas
#y la prenda seleccionadas

def df_direcciones_tallas(datos):
    dir_talla_final = []
    for talla in st.session_state.tallas_selec:
        dir_talla = datos[['direcciones','tallas']][datos['tallas']== talla]
        if len(dir_talla_final) == 0:
            dir_talla_final = dir_talla
        else:
            dir_talla_final = pd.concat([dir_talla_final, dir_talla])
    return dir_talla_final

#Puesto que las direcciones 'CALLE CONDE DE PEÑALVER, 16', 'LA MORALEJA GREEN'. No las reconoce el
#navegador porque están mal escritas. Las trtamos a parte.

def coordenadas_dir(direcciones):
    geolocator = Nominatim(user_agent="streamlit_zara")
    coordenadas = []
    for element in direcciones:
        if element not in ['CALLE CONDE DE PEÑALVER, 16', 'LA MORALEJA GREEN']:
            loc = element + ', Madrid'
            location = geolocator.geocode(loc)
            coordenadas.append([location.latitude, location.longitude])
        else:
            if element == 'CALLE CONDE DE PEÑALVER, 16':
                location = geolocator.geocode('CALLE CONDE DEL PEÑALVER, 16 , Madrid')
                coordenadas.append([location.latitude, location.longitude] )
            else:
                location = geolocator.geocode('Moraleja Green, Madrid')
                coordenadas.append([location.latitude, location.longitude] )
    return coordenadas



    
   
        