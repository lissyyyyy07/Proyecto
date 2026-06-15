import streamlit as st
import pandas as pd
from PIL import Image

from eda import eda
from ml import ml
from sm import sm
from iA import iA
from csvj import csvj
from scrapyng import scrapyng


# ======================================
# CONFIGURACIÓN
# ======================================

st.set_page_config(
    page_title="Portafolio Ciencia de Datos",
    page_icon="📊",
    layout="wide"
)


# ======================================
# ESTILOS
# ======================================

st.markdown("""
<style>

.stApp{
background:linear-gradient(to right,#081225,#0f1f3d);
}

h1,h2,h3{
color:white;
}

p{
color:white;
font-size:18px;
}

[data-testid="stSidebar"]{
background:#071224;
}

</style>
""", unsafe_allow_html=True)


# ======================================
# APP
# ======================================

def main():

    with st.sidebar:

        st.markdown("Mi Portafolio")

        menu = st.selectbox(
            "Menú",
            (
                "INICIO",
                "EDA",
                "ML",
                "SISTEMA DE RECOMENDACION",
                "Cargar archivos",
                "Análisis de sentimientos",
                "IA"
            )
        )

        st.markdown("---")

    # ======================================
    # INICIO
    # ======================================

    if menu == "INICIO":

        col1, col2 = st.columns([1, 3])

        with col1:

            try:
                imagen1 = Image.open("logo.jpg")

                st.image(
                    imagen1,
                    width=260
                )

            except:
                st.warning("Agrega logo.jpg")

        with col2:

            st.title("Karla Lisseth Lopez Herrera")

            st.subheader("Descripcion")

            st.write("""
Soy estudiante de Ingeniería en Sistemas, apasionada a la ciencia de datos.

Experiencia en:

✔ Análisis Exploratorio    
✔ Inteligencia Artificial  
✔ Visualización de Datos
            """)

        st.markdown("---")

        # KPIs
        c1, c2 = st.columns(2)

        c1.metric(
            "Tecnologías",
            "Python"
        )

        c2.metric(
            "Áreas",
            "EDA • ML • IA"
        )

        st.markdown("---")

        # TECNOLOGÍAS
        st.header("🚀 Tecnologías")

        st.write("Python")
        st.progress(95)

        st.write("Base de datos")
        st.progress(85)

        st.write("Machine Learning")
        st.progress(80)

        st.write("Java")
        st.progress(75)

        st.markdown("---")

        # VIDEO YOUTUBE
        st.header("🎥 Data Storytelling")

        youtube_url = "https://youtu.be/HQTzOubmOmI"

        st.video(youtube_url)

        st.markdown("---")

        # ÁREAS
        st.header("📌 Áreas del Portafolio")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.info("📊 EDA")

        with c2:
            st.success("🤖 Machine Learning")

        with c3:
            st.warning("🧠 IA")

        c4, c5, c6 = st.columns(3)

        with c4:
            st.info("📂 Cargar archivos")

        with c5:
            st.success("💬 Sentimientos")

        with c6:
            st.warning("🎯 Recomendación")

        st.markdown("---")


    # ======================================
    # MENÚS
    # ======================================

    elif menu == "EDA":

        try:
            df = pd.read_csv("datos.csv", sep=";")
            eda()

        except:
            st.error("No se encontró datos.csv")

    elif menu == "ML":
        ml()

    elif menu == "SISTEMA DE RECOMENDACION":
        sm()

    elif menu == "IA":
        iA()

    elif menu == "Cargar archivos":
        csvj()

    elif menu == "Análisis de sentimientos":
        scrapyng()


# ======================================
# EJECUTAR
# ======================================

if __name__ == "__main__":
    main()