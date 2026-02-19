# Manager: Jacobo cano
# Project: Dashboard - Calculadora
# Creaton Date: 11.02.2026

import streamlit as st
import polars as pl
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import altair as alt
import time                                             # Para barra de progreso
from pathlib import Path                                # Para llamar archivos en subcarpetas
from io import BytesIO
from fastexcel import read_excel

import streamlit as st

# import requests

# token_url = "https://login.microsoftonline.com/TU_TENANT_ID/oauth2/v2.0/token"

# data = {
#     "client_id": CLIENT_ID,
#     "client_secret": CLIENT_SECRET,
#     "code": auth_code,
#     "redirect_uri": REDIRECT_URI,
#     "grant_type": "authorization_code"
# }

# response = requests.post(token_url, data=data)
# tokens = response.json()
# st.write("Tokens:", tokens)

# st.write("Query params:", st.query_params)                  # Si query_params está vacío → el flujo OAuth no se está procesando.
# st.write("User:", st.user)                                  # Si st.user es None → la cookie no se está validando.
# st.write("Logged:", st.user.is_logged_in)                   # Si query_params tiene code pero is_logged_in es False → cookie_secret / redirect mismatch.

# def login_screen():
#     st.header("Esta es una aplicación privada.")
#     st.subheader("Por favor, inicie sesión.")
#     st.button("Iniciar sesión en Microsoft", on_click=st.login)

# if not st.user.is_logged_in:
#     login_screen()
# else:
#     st.header(f"Bienvenido, {st.user.name}!")
#     st.button("Cerrar sesión", on_click=st.logout)

# if "user" not in st.session_state:
#     st.session_state["user"] = {}

# st.button("Log out", on_click=st.logout)

# st.write("st.session_state object: ", st.session_state)

# ------------------------------------------------------------------------------------------------------------------------------------
# Microsoft Login
# ------------------------------------------------------------------------------------------------------------------------------------

# microsoft_login = st.button("Iniciar sesión en Microsoft", on_click=st.login)

# if microsoft_login:
#     st.login(provider="microsoft")



# logout_button = st.button("Logout")

# if logout_button:
#     st.logout()



if st.user.is_logged_in:
    st.sidebar.write(f"Hola! 👋 {st.user["name"]}")
    #st.sidebar.write(f"Sesión activa: {st.user["name"]} - {st.user["email"]}")
    if st.sidebar.button("Cerrar sesión"):
        st.logout()
else:
    if st.sidebar.button("Iniciar sesión en Microsoft", on_click=st.login):
        st.login()
        #st.login("microsoft")
        #st.write(f"{st.user["name"]} - {st.user["email"]}")
    #st.markdown(f"Welcome! {st.user["name"]} - {st.user["email"]}")
    st.stop()
        #st.login(provider="microsoft")

#st.markdown(f"Welcome! {st.user["name"]} - {st.user["email"]}")


# user_data = st.experimental_user 
# # Check if user data exists and get the name
# if user_data and user_data.get("is_logged_in", False):
#     if "name" in user_data and user_data["name"]:
#         st.write(f"User name: {user_data['name']}")
#     if "email" in user_data and user_data["email"]:
#         st.write(f"Email: {user_data['email']}")
#     if "preferred_username" in user_data and user_data["preferred_username"]:
#         st.write(f"Preferred Username: {user_data['preferred_username']}")

# ------------------------------------------------------------------------------------------------------------------------------------
# Configuración general del panel
# ------------------------------------------------------------------------------------------------------------------------------------
st.set_page_config(
    page_title="Calculadora",
    layout="wide",                      #   Muestra en modo ancho (wide)
    initial_sidebar_state="expanded"    #   Barra lateral "expandida"
    ,page_icon=":computer:"
)

# ------------------------------------------------------------------------------------------------------------------------------------
# Carga datos desde Excel
# ------------------------------------------------------------------------------------------------------------------------------------

# Configura caché para la carga una sola vez
@st.cache_data
def Cargando_datos(file_path):
    # Use polars to read, specifying engine if necessary (e.g., xlsx2csv or openpyxl)
    # xlsx2csv is often faster for big files
    return pl.read_excel(file_path)

data_folder = Path("data")
#data_file_path = data_folder / "Detalle.xlsx"
data_file_path = data_folder / "Detalle.xlsb"

# Cargar datos
if Path(data_file_path).exists():
    dataframe = Cargando_datos(data_file_path)
else:
    st.error("Archivo no encontrado.")

# ------------------------------------------------------------------------------------------------------------------------------------
# Titulo
# ------------------------------------------------------------------------------------------------------------------------------------

# Titulo en la barra lateral
media_folder = Path("media")
media_file_path = media_folder / "SEP_LOGO.png"
image = Image.open(media_file_path)
st.sidebar.image(image, width="content")

# ------------------------------------------------------------------------------------------------------------------------------------
# SideBar - Filtro: Categoria
# ------------------------------------------------------------------------------------------------------------------------------------

selected_cat = st.sidebar.selectbox(
    "Código de categoria",
    options=["Seleccione"] + dataframe
        .select(
            (
            pl.col("CODIGO_CATEGORIA")
            )
        )
        .unique()
        .sort('CODIGO_CATEGORIA')
        .to_series()
        .to_list()

    ,label_visibility="visible"
    ,index=0
)

if selected_cat == "Seleccione":
    selected_cat = None

# ------------------------------------------------------------------------------------------------------------------------------------
# SideBar - Filtro: Modelo
# ------------------------------------------------------------------------------------------------------------------------------------

# Filtra por Modelo por la Categoria seleccionada
if selected_cat:
    dataframe_filtro_mod = dataframe.filter(
        pl.col("CODIGO_CATEGORIA") == selected_cat
    )
else:
    dataframe_filtro_mod = dataframe

# Filtra por Modelo
selected_modelo = st.sidebar.selectbox(
    "Modelo",
    options=["Seleccione"] + dataframe_filtro_mod
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
# SideBar - Filtro: Nivel
# ------------------------------------------------------------------------------------------------------------------------------------

# Filtra por Nivel por la Categoria seleccionada
if selected_cat:
    dataframe_filtro_nivel = dataframe.filter(
        pl.col("CODIGO_CATEGORIA") == selected_cat
    )
else:
    dataframe_filtro_nivel = dataframe

# Filtra por Nivel por la Categoria y Modelo seleccionados
if selected_modelo:
    dataframe_filtro_nivel = dataframe.filter(
        pl.col("CODIGO_CATEGORIA") == selected_cat
        ,pl.col("MODELO") == selected_modelo
    )
else:
    dataframe_filtro_nivel = dataframe

# Filtra por Nivel
selected_nivel = st.sidebar.selectbox(
    "Nivel",
    options=["Seleccione"] + dataframe_filtro_nivel
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
# SideBar - Filtro: Zona económica
# ------------------------------------------------------------------------------------------------------------------------------------

# Filtra por Zona Económica por la Categoria seleccionada
if selected_cat:
    dataframe_filtro_ze = dataframe.filter(
        pl.col("CODIGO_CATEGORIA") == selected_cat
    )
else:
    dataframe_filtro_ze = dataframe

# Filtra por Zona Económica por la Categoria y Modelo seleccionados
if selected_modelo:
    dataframe_filtro_ze = dataframe.filter(
        pl.col("CODIGO_CATEGORIA") == selected_cat
        ,pl.col("MODELO") == selected_modelo
    )
else:
    dataframe_filtro_ze = dataframe

# Filtra por Zona Económica por la Categoria, Modelo y Nivel seleccionados
if selected_nivel:
    dataframe_filtro_ze = dataframe.filter(
        pl.col("CODIGO_CATEGORIA") == selected_cat
        ,pl.col("MODELO") == selected_modelo
        ,pl.col("NIVEL") == selected_nivel
    )
else:
    dataframe_filtro_ze = dataframe

# Filtra por Zona Económica
selected_ze = st.sidebar.selectbox(
    "Zona económica",
    options=["Seleccione"] + dataframe_filtro_ze
        .select('CVE_Z_ECONOMICA')
        .unique()
        .sort('CVE_Z_ECONOMICA')
        .to_series()
        .to_list()
    ,label_visibility="visible"
    ,index=0
)
if selected_ze == "Seleccione":
    selected_ze = None

# ------------------------------------------------------------------------------------------------------------------------------------
# SideBar - Filtro: Tipo plaza
# ------------------------------------------------------------------------------------------------------------------------------------

# Filtra por Tipo de Plaza por la Categoria seleccionada
if selected_cat:
    dataframe_filtro_tp = dataframe.filter(
        pl.col("CODIGO_CATEGORIA") == selected_cat
    )
else:
    dataframe_filtro_tp = dataframe

# Filtra por Tipo de Plaza por la Categoria y Modelo seleccionados
if selected_modelo:
    dataframe_filtro_tp = dataframe.filter(
        pl.col("CODIGO_CATEGORIA") == selected_cat
        ,pl.col("MODELO") == selected_modelo
    )
else:
    dataframe_filtro_tp = dataframe

# Filtra por Tipo de Plaza por la Categoria, Modelo y Nivel seleccionados
if selected_nivel:
    dataframe_filtro_tp = dataframe.filter(
        pl.col("CODIGO_CATEGORIA") == selected_cat
        ,pl.col("MODELO") == selected_modelo
        ,pl.col("NIVEL") == selected_nivel
    )
else:
    dataframe_filtro_tp = dataframe

# Filtra por Tipo de Plaza por la Categoria, Modelo, Nivel y Zona Económica seleccionados
if selected_ze:
    dataframe_filtro_tp = dataframe.filter(
        pl.col("CODIGO_CATEGORIA") == selected_cat
        ,pl.col("MODELO") == selected_modelo
        ,pl.col("NIVEL") == selected_nivel
        ,pl.col("CVE_Z_ECONOMICA") == selected_ze

    )
else:
    dataframe_filtro_tp = dataframe

# Filtra por Tipo de Plaza
selected_tp = st.sidebar.selectbox(
    "Tipo plaza",
    options=["Seleccione"] + dataframe_filtro_tp
        .select('TIPO_PLAZA')
        .unique()
        .sort('TIPO_PLAZA')
        .to_series()
        .to_list()
    ,label_visibility="visible"
    ,index=0
)
if selected_tp == "Seleccione":
    selected_tp = None


# ------------------------------------------------------------------------------------------------------------------------------------
# SideBar - Filtro: Entidad
# ------------------------------------------------------------------------------------------------------------------------------------

# Filtra por Entidad por la Categoria seleccionada
if selected_cat:
    dataframe_filtro_ur = dataframe.filter(
        pl.col("CODIGO_CATEGORIA") == selected_cat
    )
else:
    dataframe_filtro_ur = dataframe

# Filtra por Entidad por la Categoria y Modelo seleccionados
if selected_modelo:
    dataframe_filtro_ur = dataframe.filter(
        pl.col("CODIGO_CATEGORIA") == selected_cat
        ,pl.col("MODELO") == selected_modelo
    )
else:
    dataframe_filtro_ur = dataframe

# Filtra por Entidad por la Categoria, Modelo y Nivel seleccionados
if selected_nivel:
    dataframe_filtro_ur = dataframe.filter(
        pl.col("CODIGO_CATEGORIA") == selected_cat
        ,pl.col("MODELO") == selected_modelo
        ,pl.col("NIVEL") == selected_nivel
    )
else:
    dataframe_filtro_ur = dataframe

# Filtra por Entidad por la Categoria, Modelo, Nivel y Zona Económica seleccionados
if selected_ze:
    dataframe_filtro_ur = dataframe.filter(
        pl.col("CODIGO_CATEGORIA") == selected_cat
        ,pl.col("MODELO") == selected_modelo
        ,pl.col("NIVEL") == selected_nivel
        ,pl.col("CVE_Z_ECONOMICA") == selected_ze

    )
else:
    dataframe_filtro_ur = dataframe

# Filtra por Entidad por la Categoria, Modelo, Nivel, Zona Económica y Tipo de Plaza seleccionados
if selected_tp:
    dataframe_filtro_ur = dataframe.filter(
        pl.col("CODIGO_CATEGORIA") == selected_cat
        ,pl.col("MODELO") == selected_modelo
        ,pl.col("NIVEL") == selected_nivel
        ,pl.col("CVE_Z_ECONOMICA") == selected_ze
        ,pl.col("TIPO_PLAZA") == selected_tp
    )
else:
    dataframe_filtro_ur = dataframe

# Filtra por Entidad
selected_ur = st.sidebar.selectbox(
    "Entidad",
    options=["Seleccione"] + dataframe_filtro_ur
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
# SideBar - Filtro: Número de plazas y Número de horas
# ------------------------------------------------------------------------------------------------------------------------------------

txt_plazas = st.sidebar.text_input(
    "Número de plazas"
    ,value = 0
)

# Solo si se selecciona "H" (Horas) se muestra el cuadro de texto
if selected_tp == "H":
    txt_horas = st.sidebar.text_input(
        "Número de horas"
        ,value = 0
    )

# ------------------------------------------------------------------------------------------------------------------------------------
# Panel central: Muestra (descripción de) la Categoría *******************************************************************************
# ------------------------------------------------------------------------------------------------------------------------------------
if selected_cat:
    categorias = dataframe[["CODIGO_CATEGORIA", "CATEGORIA", "MODELO", "NIVEL", "CVE_Z_ECONOMICA", "TIPO_PLAZA", "ENTIDAD_FEDERATIVA"]].unique()

    if selected_modelo:
        categoria = (
            categorias.filter(
                pl.col("CODIGO_CATEGORIA") == selected_cat
                ,pl.col("MODELO") == selected_modelo
                )
            .select(["CATEGORIA", "MODELO"])
                    .unique()
                    .sort(
                        by=["CATEGORIA", "MODELO"]
                        ,descending=[False, False]
                        )
        )

        if selected_nivel:
            categoria = (
                categorias.filter(
                    (pl.col("CODIGO_CATEGORIA") == selected_cat) &
                    (pl.col("MODELO") == selected_modelo) &
                    (pl.col("NIVEL") == selected_nivel)
                    )
                .select(["CATEGORIA", "MODELO", "NIVEL"])
                        .unique()
                        .sort(
                                by=["CATEGORIA", "MODELO", "NIVEL"]
                                ,descending=[False, False, False]
                            )
            )


            if selected_ze:
                categoria = (
                    categorias.filter(
                        (pl.col("CODIGO_CATEGORIA") == selected_cat) &
                        (pl.col("MODELO") == selected_modelo) &
                        (pl.col("NIVEL") == selected_nivel) &
                        (pl.col("CVE_Z_ECONOMICA") == selected_ze)
                        )
                    .select(["CATEGORIA", "MODELO", "NIVEL", "CVE_Z_ECONOMICA"])
                            .unique()
                            .sort(
                                    by=["CATEGORIA", "MODELO", "NIVEL", "CVE_Z_ECONOMICA"]
                                    ,descending=[False, False, False, False]
                                )
                )


                if selected_tp:
                    categoria = (
                        categorias.filter(
                            (pl.col("CODIGO_CATEGORIA") == selected_cat) &
                            (pl.col("MODELO") == selected_modelo) &
                            (pl.col("NIVEL") == selected_nivel) &
                            (pl.col("CVE_Z_ECONOMICA") == selected_ze) &
                            (pl.col("TIPO_PLAZA") == selected_tp)
                            )
                        .select(["CATEGORIA", "MODELO", "NIVEL", "CVE_Z_ECONOMICA", "TIPO_PLAZA"])
                                .unique()
                                .sort(
                                        by=["CATEGORIA", "MODELO", "NIVEL", "CVE_Z_ECONOMICA", "TIPO_PLAZA"]
                                        ,descending=[False, False, False, False, False]
                                    )
                    )

                    if selected_ur:
                        categoria = (
                            categorias.filter(
                                (pl.col("CODIGO_CATEGORIA") == selected_cat) &
                                (pl.col("MODELO") == selected_modelo) &
                                (pl.col("NIVEL") == selected_nivel) &
                                (pl.col("CVE_Z_ECONOMICA") == selected_ze) &
                                (pl.col("TIPO_PLAZA") == selected_tp) &
                                (pl.col("ENTIDAD_FEDERATIVA") == selected_ur)
                                )
                            .select(["CATEGORIA", "MODELO", "NIVEL", "CVE_Z_ECONOMICA", "TIPO_PLAZA", "ENTIDAD_FEDERATIVA"])
                                    .unique()
                                    .sort(
                                            by=["CATEGORIA", "MODELO", "NIVEL", "CVE_Z_ECONOMICA", "TIPO_PLAZA", "ENTIDAD_FEDERATIVA"]
                                            ,descending=[False, False, False, False, False, False]
                                        )
                        )
                        st.write("", selected_cat + ' ' + categoria["CATEGORIA"] + ', MODELO  ' + categoria["MODELO"] + ', NIVEL  ' + categoria["NIVEL"] + ', ZONA ECONÓMICA  ' + categoria["CVE_Z_ECONOMICA"] + ', TIPO PLAZA  ' + categoria["TIPO_PLAZA"] + ', ENTIDAD  ' + categoria["ENTIDAD_FEDERATIVA"])

                    else:
                        st.write("", selected_cat + ' ' + categoria["CATEGORIA"] + ', MODELO  ' + categoria["MODELO"] + ', NIVEL  ' + categoria["NIVEL"] + ', ZONA ECONÓMICA  ' + categoria["CVE_Z_ECONOMICA"] + ', TIPO PLAZA  ' + categoria["TIPO_PLAZA"])

                else:
                    st.write("", selected_cat + ' ' + categoria["CATEGORIA"] + ', MODELO  ' + categoria["MODELO"] + ', NIVEL  ' + categoria["NIVEL"] + ', ZONA ECONÓMICA  ' + categoria["CVE_Z_ECONOMICA"])

            else:
                st.write("", selected_cat + ' ' + categoria["CATEGORIA"] + ', MODELO  ' + categoria["MODELO"] + ', NIVEL  ' + categoria["NIVEL"])

        else:
            st.write("", selected_cat + ' ' + categoria["CATEGORIA"] + ', MODELO  ' + categoria["MODELO"])

    else:
        categoria = (
            categorias.filter(
                pl.col("CODIGO_CATEGORIA") == selected_cat
                )
            .select(
                pl.col("CATEGORIA")
                    .sort()
                    .unique()
                )
        )
        st.write("", selected_cat + ' ' + categoria)

# ------------------------------------------------------------------------------------------------------------------------------------
# Panel central: Datagrid - Columnas
# ------------------------------------------------------------------------------------------------------------------------------------

df_calculadora = (
    dataframe
    .select(pl.col("ENTIDAD_FEDERATIVA").alias('ENTIDAD')
        ,pl.col("CODIGO_CATEGORIA").alias("CODIGO_CATEGORIA")
        ,pl.col("CATEGORIA").alias("CATEGORIA")
        ,pl.col("CLASIFICACION").alias('CLASIFICACION')
        ,pl.col("TIPO_PLAZA").alias('TIPO PLAZA')

        ,pl.col("MODELO").alias('MODELO')
        ,pl.col("NIVEL").alias('NIVEL')
        ,pl.col("CVE_Z_ECONOMICA").alias('ZONA ECONÓMICA')
        ,pl.col("MODALIDAD").alias('MODALIDAD')

        ,pl.col("CONCEPTO").alias('CONCEPTO PAGO')
        #,pl.col("CONCEPTO_DE_PAGO").alias('CONCEPTO DE PAGO')

        #,pl.col("CODIGO_FEDERAL").alias('CODIGO_FEDERAL')
        #,pl.col("CODIGO_ESTATAL").alias('CODIGO_ESTATAL')
        ,pl.col("AMBITO_APLICATIVO").alias('AMBITO APLICATIVO')

        ,pl.col("PERIODICIDAD").alias('PERIODICIDAD')
        ,pl.col("GRAVABLE").alias('GRAVABLE')
        ,pl.col("HRS_DE_COMPATIBILIDAD").alias('HRS_DE_COMPATIBILIDAD')

        ,pl.col("ENERO").alias('ENERO')
        ,pl.col("FEBRERO").alias('FEBRERO')
        ,pl.col("MARZO").alias('MARZO')
        ,pl.col("ABRIL").alias('ABRIL')

        ,pl.col("MAYO").alias('MAYO')
        ,pl.col("JUNIO").alias('JUNIO')
        ,pl.col("JULIO").alias('JULIO')
        ,pl.col("AGOSTO").alias('AGOSTO')

        ,pl.col("SEPTIEMBRE").alias('SEPTIEMBRE')
        ,pl.col("OCTUBRE").alias('OCTUBRE')
        ,pl.col("NOVIEMBRE").alias('NOVIEMBRE')
        ,pl.col("DICIEMBRE").alias('DICIEMBRE')

        ,pl.col("COSTO_UNITARIO_ANUAL").alias('COSTO UNITARIO ANUAL')

    )
)

# ------------------------------------------------------------------------------------------------------------------------------------
# Panel central: Datagrid - Filtro: Categoria *
# ------------------------------------------------------------------------------------------------------------------------------------

if selected_cat:
    df_calculadora = df_calculadora.filter(
        pl.col('CODIGO_CATEGORIA') == selected_cat
    )

# ------------------------------------------------------------------------------------------------------------------------------------
# Panel central: Datagrid - Filtro: Modelo
# ------------------------------------------------------------------------------------------------------------------------------------

if selected_modelo:
    df_calculadora = df_calculadora.filter(
        pl.col('MODELO') == selected_modelo
    )

# ------------------------------------------------------------------------------------------------------------------------------------
# Panel central: Datagrid - Filtro: Nivel
# ------------------------------------------------------------------------------------------------------------------------------------

if selected_nivel:
    df_calculadora = df_calculadora.filter(
        pl.col('NIVEL') == selected_nivel
    )

# ------------------------------------------------------------------------------------------------------------------------------------
# Panel central: Datagrid - Zona Económica
# ------------------------------------------------------------------------------------------------------------------------------------

if selected_ze:
    df_calculadora = df_calculadora.filter(
        pl.col('ZONA ECONÓMICA') == selected_ze
    )

# ------------------------------------------------------------------------------------------------------------------------------------
# Panel central: Datagrid - Tipo Plaza
# ------------------------------------------------------------------------------------------------------------------------------------

if selected_tp:
    df_calculadora = df_calculadora.filter(
        pl.col('TIPO PLAZA') == selected_tp
    )

# ------------------------------------------------------------------------------------------------------------------------------------
# Panel central: Datagrid - Entidad
# ------------------------------------------------------------------------------------------------------------------------------------

if selected_ur:
    df_calculadora = df_calculadora.filter(
    pl.col('ENTIDAD') == selected_ur
)

# ------------------------------------------------------------------------------------------------------------------------------------
# Panel central: - Muestra Textbox: Costo Total
# ------------------------------------------------------------------------------------------------------------------------------------
if txt_plazas and int(txt_plazas) > 0:
    if selected_tp == "H" :
        if txt_horas:
            costo_total = int(txt_plazas) * int(txt_horas)
            txt_costo_total = {type(costo_total)}
            # st.text_input("COSTO TOTAL ", costo_total, width=125)
        else:
            costo_total = 0

    else:
        costo_total = int(txt_plazas)
        txt_costo_total = {type(costo_total)}
        # st.text_input("COSTO TOTAL ", costo_total, width=125)


# ------------------------------------------------------------------------------------------------------------------------------------
# Panel central: Gridview con Calendario (enero - diciembre)
# ------------------------------------------------------------------------------------------------------------------------------------
    # costo_total = 1
    if selected_cat:
        df_calculadora_totales = (
            df_calculadora
            .select(

                pl.col("COSTO UNITARIO ANUAL").sum().alias('COSTO TOTAL ANUAL') * costo_total

                ,pl.col("ENERO").sum().alias('ENE') * costo_total
                ,pl.col("FEBRERO").sum().alias('FEB') * costo_total
                ,pl.col("MARZO").sum().alias('MAR') * costo_total
                ,pl.col("ABRIL").sum().alias('ABR') * costo_total

                ,pl.col("MAYO").sum().alias('MAY') * costo_total
                ,pl.col("JUNIO").sum().alias('JUN') * costo_total
                ,pl.col("JULIO").sum().alias('JUL') * costo_total
                ,pl.col("AGOSTO").sum().alias('AGO') * costo_total

                ,pl.col("SEPTIEMBRE").sum().alias('SEP') * costo_total
                ,pl.col("OCTUBRE").sum().alias('OCT') * costo_total
                ,pl.col("NOVIEMBRE").sum().alias('NOV') * costo_total
                ,pl.col("DICIEMBRE").sum().alias('DIC') * costo_total



            )
        )

        st.data_editor(
            df_calculadora_totales,
            column_config={

                "ENE": st.column_config.NumberColumn(format="accounting"),
                "FEB": st.column_config.NumberColumn(format="accounting"),
                "MAR": st.column_config.NumberColumn(format="accounting"),
                "ABR": st.column_config.NumberColumn(format="accounting"),

                "MAY": st.column_config.NumberColumn(format="accounting"),
                "JUN": st.column_config.NumberColumn(format="accounting"),
                "JUL": st.column_config.NumberColumn(format="accounting"),
                "AGO": st.column_config.NumberColumn(format="accounting"),

                "SEP": st.column_config.NumberColumn(format="accounting"),
                "OCT": st.column_config.NumberColumn(format="accounting"),
                "NOV": st.column_config.NumberColumn(format="accounting"),
                "DIC": st.column_config.NumberColumn(format="accounting"),

                "COSTO TOTAL ANUAL": st.column_config.NumberColumn(format="accounting")
            },
            #use_container_width=True,
            width="stretch"
            ,disabled=True
            ,hide_index=True
        )

# ------------------------------------------------------------------------------------------------------------------------------------
# Panel central: Carga dataframe y aplica formato a algunas columnas
# ------------------------------------------------------------------------------------------------------------------------------------
if selected_cat:
#if selected_cat and selected_modelo and selected_nivel and selected_ze and selected_tp and selected_ur:
    st.data_editor(
        df_calculadora,
        column_config={

            # Thousands separator (integers)

            "HRS_DE_COMPATIBILIDAD": st.column_config.NumberColumn(format="localized"),

            # Currency formatting

            "ENERO": st.column_config.NumberColumn(format="accounting"),
            "FEBRERO": st.column_config.NumberColumn(format="accounting"),
            "MARZO": st.column_config.NumberColumn(format="accounting"),
            "ABRIL": st.column_config.NumberColumn(format="accounting"),

            "MAYO": st.column_config.NumberColumn(format="accounting"),
            "JUNIO": st.column_config.NumberColumn(format="accounting"),
            "JULIO": st.column_config.NumberColumn(format="accounting"),
            "AGOSTO": st.column_config.NumberColumn(format="accounting"),

            "SEPTIEMBRE": st.column_config.NumberColumn(format="accounting"),
            "OCTUBRE": st.column_config.NumberColumn(format="accounting"),
            "NOVIEMBRE": st.column_config.NumberColumn(format="accounting"),
            "DICIEMBRE": st.column_config.NumberColumn(format="accounting"),

            "COSTO UNITARIO ANUAL": st.column_config.NumberColumn(format="accounting"),
        },
        #use_container_width=True,
        width="stretch"
        ,disabled=True
        ,hide_index=True
    )
