# Manager: Jacobo cano
# Project: Dashboard - Calculadora
# Creaton Date: 11.02.2026

import streamlit as st
import polars as pl
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import altair as alt

# ------------------------------------------------------------------------------------------------------------------------------------
# Configuración general del panel
# ------------------------------------------------------------------------------------------------------------------------------------
st.set_page_config(
    page_title="Calculadora",
    layout="wide", # This sets the app to wide mode
    initial_sidebar_state="expanded" # Optional: control sidebar state
)

# ------------------------------------------------------------------------------------------------------------------------------------
# Carga datos desde Excel
# ------------------------------------------------------------------------------------------------------------------------------------
# Dataset of Employee's Data
dataframe = pl.read_excel('Calculadora 2026 v02.xlsx')



# ------------------------------------------------------------------------------------------------------------------------------------
# Logotipo
# ------------------------------------------------------------------------------------------------------------------------------------
# image = Image.open('SEP_LOGO.png')
# st.image(image, width="content")

# ------------------------------------------------------------------------------------------------------------------------------------
# Titulo
# ------------------------------------------------------------------------------------------------------------------------------------
st.title('Calculadora.')
# st.subheader('Febrero 2026')


# Titulo en la barra lateral

image = Image.open('SEP_LOGO.png')
st.sidebar.image(image, width="content")
# st.sidebar.title("Calculadora 📄")
st.sidebar.caption(" Filtros: ")

# ------------------------------------------------------------------------------------------------------------------------------------
# SideBar
# ------------------------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------------------------------
# SideBar - Entidad
# ------------------------------------------------------------------------------------------------------------------------------------

selected_ur = st.sidebar.selectbox(
    "Entidad",
    options=["Seleccione"] + dataframe
        .select('ENTIDAD_FEDERATIVA')
        .unique()
        .sort('ENTIDAD_FEDERATIVA')
        .to_series()
        .to_list()
    ,label_visibility="visible"
    ,index=0
)
if selected_ur == "Seleccione":
    selected_ur = None

# ------------------------------------------------------------------------------------------------------------------------------------
# SideBar - Categoria
# ------------------------------------------------------------------------------------------------------------------------------------

# Filtra categorias de la entidad seleccionada
if selected_ur:
    # Use Polars filter syntax: df.filter(condition_1)
    dataframe_filtro_ur = dataframe.filter(
        pl.col('ENTIDAD_FEDERATIVA') == selected_ur
    )
else:
    dataframe_filtro_ur = dataframe

selected_cat = st.sidebar.selectbox(
    "Categoria",    
    options=["Seleccione"] + dataframe_filtro_ur
        .select(
            (
            pl.col("CODIGO_CATEGORIA") + ' ' + pl.col("CATEGORIA")
            ).alias("CATEGORIA")
            
        )
        .unique()
        .sort('CATEGORIA')
        .to_series()
        .to_list()        
        
    ,label_visibility="visible"
    ,index=0
)
if selected_cat == "Seleccione":
    selected_cat = None

# ------------------------------------------------------------------------------------------------------------------------------------
# SideBar - Modelo
# ------------------------------------------------------------------------------------------------------------------------------------

# Filtra modelos de la categoria seleccionada
if selected_cat:
    # Use Polars filter syntax: df.filter(condition_1)
    dataframe_filtro_cat = dataframe.filter(
        pl.col('CATEGORIA') == selected_cat
    )
else:
    dataframe_filtro_cat = dataframe


selected_modelo = st.sidebar.selectbox(
    "Modelo",
    options=["Seleccione"] + dataframe_filtro_cat
        .select('MODELO')
        .unique()
        .sort('MODELO')
        .to_series()
        .to_list()
    ,label_visibility="visible"
    ,index=0
)
if selected_modelo == "Seleccione":
    selected_modelo = None

# ------------------------------------------------------------------------------------------------------------------------------------
# SideBar - Nivel
# ------------------------------------------------------------------------------------------------------------------------------------

selected_nivel = st.sidebar.selectbox(
    "Nivel",
    options=["Seleccione"] + dataframe
        .select('NIVEL')
        .unique()
        .sort('NIVEL')
        .to_series()
        .to_list()
    ,label_visibility="visible"
    ,index=0
)
if selected_nivel == "Seleccione":
    selected_nivel = None

# ------------------------------------------------------------------------------------------------------------------------------------
# Zona económica
# ------------------------------------------------------------------------------------------------------------------------------------

selected_ze = st.sidebar.selectbox(
    "Zona económica",
    options=["Seleccione"] + dataframe
        .select('CVE_ZONA_ECONOMICA')
        .unique()
        .sort('CVE_ZONA_ECONOMICA')
        .to_series()
        .to_list()
    ,label_visibility="visible"
    ,index=0
)
if selected_ze == "Seleccione":
    selected_ze = None


# ------------------------------------------------------------------------------------------------------------------------------------
# 	Datagrid
# ------------------------------------------------------------------------------------------------------------------------------------

st.markdown("""
<hr style="height:2px;border:none;color:#333;background-color:#333;" />
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------------------------------------------------------------
# 	Datagrid - Columnas
# ------------------------------------------------------------------------------------------------------------------------------------

df_calculadora = (
    dataframe    
    .select(pl.col("ENTIDAD_FEDERATIVA").alias('ENTIDAD')
        #,pl.col("CODIGO_CATEGORIA").alias("CODIGO_CATEGORIA")
        #,pl.col("CATEGORIA").alias("CATEGORIA")
        ,pl.col("CODIGO_CATEGORIA") + pl.lit(" ") + pl.col("CATEGORIA").cast(pl.String).alias("CATEGORIA")
        ,pl.col("MODELO").alias('MODELO')
        ,pl.col("NIVEL").alias('NIVEL')
        ,pl.col("CVE_ZONA_ECONOMICA").alias('ZONA ECONÓMICA')
        ,pl.col("TIPO_PLAZA").alias('TIPO PLAZA')
        ,pl.col("CONCEPTO_DE_PAGO").alias('CONCEPTO DE PAGO')
        ,pl.col("CODIGO_CPTO_PAGO_FEDERAL").alias('CPTO PAGO FEDERAL')
        ,pl.col("CODIGO_CPTO_PAGO_ESTATAL").alias('CPTO PAGO ESTATAL')
        ,pl.col("AMBITO_APLICATIVO").alias('AMBITO APLICATIVO')
        ,pl.col("PERIODICIDAD").alias('PERIODICIDAD')
        ,pl.col("GRAVABLE").alias('GRAVABLE')
        ,pl.col("CANT_HRS_COMP").alias('CANT HRS COMP')
        ,pl.col("CANT_PZAS_HORAS").alias('CANT PZAS HORAS')
        ,pl.col("CANT_PLAZAS").alias('CANT PLAZAS')
        ,pl.col("IMPORTE UNITARIO").alias('IMPORTE UNITARIO')
        ,pl.col("COSTO_UNITARIO_ANUAL").alias('COSTO UNITARIO ANUAL')
        ,pl.col("COSTO ANUAL").alias('COSTO ANUAL')
        ,pl.col("COSTO ANUAL SECORE SIN HRS COMP").alias('COSTO ANUAL SECORE SIN HRS COMP')
        ,pl.col("COSTO ANUAL CN SIN HRS COMP").alias('COSTO ANUAL CN SIN HRS COMP')
    )    
    #.filter(pl.col("ENTIDAD") == selected_ur)    
)



# if selected_ur:
#     df_calculadora = df_calculadora.filter(
#         pl.col("ENTIDAD") == selected_ur
#     )


# 3. Apply filters to the DataFrame
# filtered_df = df_calculadora

#if selected_ur != 'Seleccione':


# ------------------------------------------------------------------------------------------------------------------------------------
# 	Filtros - Entidad
# ------------------------------------------------------------------------------------------------------------------------------------

if selected_ur:
    # Use Polars filter syntax: df.filter(condition_1)
    df_calculadora = df_calculadora.filter(
        pl.col('ENTIDAD') == selected_ur
    )

# ------------------------------------------------------------------------------------------------------------------------------------
# 	Filtros - Categoria *
# ------------------------------------------------------------------------------------------------------------------------------------

#if selected_ur:
    # Use Polars filter syntax: df.filter(condition_1)
    # df_calculadora = dataframe.filter(
    # pl.col('ENTIDAD_FEDERATIVA') == selected_ur
#)
#else:
#    df_calculadora = dataframe

if selected_cat:
    #df_calculadora = dataframe.filter(
    #    pl.col('ENTIDAD_FEDERATIVA') == selected_ur
    #)
    # Combine conditions using the logical AND operator (&): df.filter(condition_1 & condition_2)
    df_calculadora = df_calculadora.filter(
        pl.col('CODIGO_CATEGORIA') == selected_cat
    )

# ------------------------------------------------------------------------------------------------------------------------------------
# 	Filtros - Modelo
# ------------------------------------------------------------------------------------------------------------------------------------

if selected_modelo:
    df_calculadora = df_calculadora.filter(
        pl.col('MODELO') == selected_modelo
    )

# # ------------------------------------------------------------------------------------------------------------------------------------
# # 	Filtros - Nivel
# # ------------------------------------------------------------------------------------------------------------------------------------

if selected_nivel:
    df_calculadora = df_calculadora.filter(
        pl.col('NIVEL') == selected_nivel
    )

# # ------------------------------------------------------------------------------------------------------------------------------------
# # 	Filtros - Zona Económica
# # ------------------------------------------------------------------------------------------------------------------------------------

if selected_ze:
    df_calculadora = df_calculadora.filter(
        pl.col('ZONA ECONÓMICA') == selected_ze
    )



# ------------------------------------------------------------------------------------------------------------------------------------
# 	Formato - Columnas
# ------------------------------------------------------------------------------------------------------------------------------------

st.data_editor(
    df_calculadora,
    column_config={

        # Thousands separator (integers)
        "CANT HRS COMP": st.column_config.NumberColumn(format="localized"),
        "CANT PZAS HORAS": st.column_config.NumberColumn(format="localized"),
        "CANT PLAZAS": st.column_config.NumberColumn(format="localized"),

        # Currency formatting
        "IMPORTE UNITARIO": st.column_config.NumberColumn(format="accounting"),
        "COSTO UNITARIO ANUAL": st.column_config.NumberColumn(format="accounting"),
        "COSTO ANUAL": st.column_config.NumberColumn(format="accounting"),
        "COSTO ANUAL SECORE SIN HRS COMP": st.column_config.NumberColumn(format="accounting"),
        "COSTO ANUAL CN SIN HRS COMP": st.column_config.NumberColumn(format="accounting"),
    },
    use_container_width=True,
    disabled=True
)
