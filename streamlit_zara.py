import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from zara_functions_streamlit_buscador import *
from zara_functions_streamlit_mapa import *
import folium
from geopy.geocoders import Nominatim 
import base64


st.set_page_config(layout="wide", page_title='Nueva colección Zara')

#Confiuración del fondo:
    
with open('6392ad594f71e.jpeg', "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
st.markdown(
f"""
<style>
.stApp {{
    background-image: url(data:image/{"jpeg"};base64,{encoded_string.decode()});
    background-size: cover
}}
</style>
""",
unsafe_allow_html=True
)

st.title('ZARA')
                                   
st.write( "Una aplicación para poder ver la Nueva Colección de Zara" )
datos = pd.read_csv('datos_zara_procesados.csv')

#Creamos la columna pie_foto para poner la descripción en el buscador

datos['pie_foto'] = datos['nombre_prenda'] +', \n'+ datos['precio_prenda'].apply(str) + '€'


menu = st.sidebar.radio(
    "",
    ("Buscador", "Disponibilidad en tienda", "Análisis tiendas"),
)


#######################

if menu == 'Buscador':
    st.header('Buscador :mag_right:')
    st.radio(
        "Elige el método de búsqueda",
        key="tipo_busqueda",
        options=["Nombre prenda", "Tipo prenda", "Intervalo de precio"],
    )
    
    if st.session_state.tipo_busqueda == "Nombre prenda":
        buscador_prenda(datos)
            
    elif st.session_state.tipo_busqueda == "Tipo prenda":
        buscador_tipo_prenda(datos)
                   
    else:
        buscador_intervalo_precios(datos)

    
    
#########################

elif menu == "Análisis tiendas":

    st.header("Análisis tiendas")
    st.selectbox("Elige la acción que deseas realizar",('Número de prendas por tienda de Zara y por tipo'
                                                        ,'Ver la diferencia de precios entre los tipos de prendas'
                                                        ,''),key = "opc_analisis")
    if st.session_state.opc_analisis == 'Número de prendas por tienda de Zara y por tipo':
        df_prendas_tienda = datos[['nombre_prenda','direcciones', 'tipo_prenda']].groupby(['direcciones','tipo_prenda']).count().reset_index()
        df_prendas_tienda.rename({'nombre_prenda' : 'numero_prendas'}, axis = 1, inplace = True)
        st.dataframe(df_prendas_tienda)
        
        if st.checkbox('¿Desea ver este resultado gráficamente?'):
            fig = px.bar(df_prendas_tienda, x = 'direcciones', y = 'numero_prendas'
                         , color = 'tipo_prenda'
                         , title = 'Número de prendas por tipo de prenda y dirección'
                         , labels = {'numero_prendas' : 'Número de prendas'
                                     , 'tipo_prenda': 'Tipo de prenda'}
                         , template="simple_white")
            st.plotly_chart(fig)

    else: 

        fig = px.scatter(datos, x="tipo_prenda", y="precio_prenda",            
                color="tipo_prenda", 
                title = "Precio por tipo de prenda",
                labels = {"tipo_prenda" : "Tipo de prenda",
                          "precio_prenda" : "Precio prenda"},
                template="simple_white",
                color_discrete_sequence=px.colors.qualitative.Alphabet)
        fig.update_traces(marker_size=10)
        st.plotly_chart(fig)

        fig = px.box(datos, x="tipo_prenda", y="precio_prenda", color="tipo_prenda",
                     title = "Precio por tipo de prenda",
                     labels = {"tipo_prenda" : "Tipo de prenda",
                               "precio_prenda" : "Precio prenda"},
                     template="simple_white",
                     notched=True)
        st.plotly_chart(fig)

else:
    st.text_input("Escribe el nombre de la prenda que quieres buscar", key="buscador", value = "MONO LARGO CARGO")
    prenda = buscador_prenda_mapa(datos,st.session_state.buscador)
    if len(prenda) > 0:
        tallas = datos['tallas'][datos['nombre_prenda'] == prenda[0]].unique()
        tallas = list(tallas)
        if st.multiselect('Seleccione las tallas a buscar',options = tallas, key = "tallas_selec"):
            if st.checkbox('Buscar', key = 'buscar'):
               
                #Nos creamos un conjunto de datos que solo tengas las columnas que nos interesan
                
                datos = datos[['nombre_prenda','direcciones', 'tallas']][datos['nombre_prenda'] == prenda[0]]
                dir_talla_final = df_direcciones_tallas(datos)
                
                #Mediante el paquete geopy, calculamos las coordenadas de las direcciones
                direcciones = list(dir_talla_final['direcciones'].unique())
                coordenadas = coordenadas_dir(direcciones)
                
                #Creamos el mapa
                mapa = folium.Map(location= [40.47083205, -3.871344282431271], zoom_start = 10)
                
                tooltip = "Haz click para obtener más información"
                
                for i in range(len(coordenadas)):
                    tallas = dir_talla_final['tallas'][dir_talla_final['direcciones'] == direcciones[i]].unique()
                    texto = direcciones[i] + ', Tallas :'
                    for j in range(len(tallas)):
                        if j != len(tallas)-1:
                            texto += tallas[j] + ', ' 
                        else:
                            texto+= tallas[j]
                    marker = folium.Marker(
                        location=coordenadas[i],
                        popup=folium.Popup(texto),
                        tooltip=tooltip)
                
                    marker.add_to(mapa)
                mapa
    
    else:
        st.write('No se ha encontrado la prenda seleccionada')
   
     
        