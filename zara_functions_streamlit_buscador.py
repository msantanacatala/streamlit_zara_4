import streamlit as st
import numpy as np

#datos: nuestro dataset
#columna: la columna sobre la que queremos filtrar la búsqueda
#key: la clave del input correspondiente

def quitar_acentos(palabra):
    acentos = ['Á', 'É', 'Í', 'Ó', 'Ú']
    no_acentos = ['A', 'E', 'I', 'O', 'U']
    for letra in palabra:
        if letra in acentos:
            posc = acentos.index(letra)
            palabra = palabra.replace(letra, no_acentos[posc])
    return palabra 

def seleccion_imagenes_tipo_prenda(datos,columna,key):
    imagenes_selec = list(datos['imagen_prenda'][datos[columna]== key].unique())
    descripciones_selec = list(datos['pie_foto'][datos[columna]== key].unique()) 
    return [imagenes_selec, descripciones_selec]

def impresion_imagenes_columnas(imagenes_selec, descripciones_selec):
    col1, col2, col3, col4 = st.columns(4)
    for i in range (len(descripciones_selec)): #porque a veces hay más de un color por prenda
        if i%4 == 0:
            col1.image(imagenes_selec[i], caption = descripciones_selec[i])
        elif i%4 == 1:
            col2.image(imagenes_selec[i], caption = descripciones_selec[i])
        elif i%4 == 2:
            col3.image(imagenes_selec[i], caption = descripciones_selec[i])
        else:
            col4.image(imagenes_selec[i], caption = descripciones_selec[i])
            
def selector_rango_precios(datos, columna):
    parte_entera_maximo = int(max(datos[columna])) + 1 #mas uno porque la parte entera es inferior
    #al valor original
    st.slider('Elige una cota inferior', 0, parte_entera_maximo, 50, key = 'cota_inferior')
    
    media_minimo_maximo = np.mean([parte_entera_maximo,st.session_state.cota_inferior])
    
    st.slider('Elige una cota superior', st.session_state.cota_inferior, parte_entera_maximo, 
              int(media_minimo_maximo), 
              key = 'cota_superior')
    
    st.write('Prendas entre', str(st.session_state.cota_inferior), '€ y ', str(st.session_state.cota_superior), '€')

def seleccion_imagenes_rango_precios(datos,columna):
    imagenes_selec = list(datos['imagen_prenda'][(datos[columna]>= st.session_state.cota_inferior) 
                                        & (datos[columna]<= st.session_state.cota_superior)].unique())
    descripciones_selec = list(datos['pie_foto'][(datos[columna]>= st.session_state.cota_inferior) 
                                        & (datos[columna]<= st.session_state.cota_superior)].unique())
    return [imagenes_selec, descripciones_selec]
    
def buscador_prenda(datos):
    st.text_input("Escribe el nombre de la prenda que quieres buscar", key="buscador", value = "MONO LARGO CARGO")
    prenda = st.session_state.buscador.upper()
    prenda = quitar_acentos(prenda) 
    imagen_selec = datos['imagen_prenda'][datos['nombre_prenda'] == prenda].unique()
    imagen_selec = list(imagen_selec)
    if len(imagen_selec) > 0:
        st.image(imagen_selec)
    else:
        st.write('No se ha encontrado la prenda seleccionada')

        
def buscador_tipo_prenda(datos):
    st.selectbox("Elige el tipo de prenda",tuple(datos['tipo_prenda'].unique()), key = "tipo_prenda")
    imagenes_selec, descripciones_selec = seleccion_imagenes_tipo_prenda(datos,'tipo_prenda',st.session_state.tipo_prenda)
    if len(imagenes_selec)>0:       
        impresion_imagenes_columnas(imagenes_selec, descripciones_selec)
    else:
        st.write('No se ha encontrado este artículo')
        
def buscador_intervalo_precios(datos):
    selector_rango_precios(datos, 'precio_prenda')
    imagenes_selec, descripciones_selec = seleccion_imagenes_rango_precios(datos,'precio_prenda')
    if len(imagenes_selec) > 0:
        impresion_imagenes_columnas(imagenes_selec, descripciones_selec)
    else:
        st.write('No se ha encontrado este artículo')