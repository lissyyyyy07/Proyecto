# =========================================================
# SISTEMA DE RECOMENDACIÓN DE LIBROS
# NIVEL SENIOR - STREAMLIT + MACHINE LEARNING
# =========================================================

# =========================================================
# IMPORTACIONES
# =========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="Sistema de Recomendación de Libros",
    page_icon="📚",
    layout="wide"
)

# =========================================================
# ESTILOS
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #0F172A;
    color: white;
}

h1, h2, h3 {
    color: #38BDF8;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

div[data-testid="metric-container"] {
    background-color: #1E293B;
    border-radius: 15px;
    padding: 15px;
    border: 1px solid #334155;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# FUNCIÓN PRINCIPAL
# =========================================================

def sm():

    # =====================================================
    # DATASET
    # =====================================================

    @st.cache_data
    def cargar_datos():

        datos = {

            "Titulo": [
                "Harry Potter",
                "El Señor de los Anillos",
                "Cien Años de Soledad",
                "Orgullo y Prejuicio",
                "1984",
                "Don Quijote",
                "Los Juegos del Hambre",
                "Percy Jackson",
                "The Hobbit",
                "Crónica de una Muerte Anunciada"
            ],

            "Autor": [
                "J.K Rowling",
                "J.R.R Tolkien",
                "Gabriel García Márquez",
                "Jane Austen",
                "George Orwell",
                "Miguel de Cervantes",
                "Suzanne Collins",
                "Rick Riordan",
                "J.R.R Tolkien",
                "Gabriel García Márquez"
            ],

            "Genero": [
                "Fantasía",
                "Fantasía",
                "Realismo Mágico",
                "Romance",
                "Distopía",
                "Clásico",
                "Ciencia Ficción",
                "Fantasía",
                "Fantasía",
                "Drama"
            ],

            "Descripcion": [
                "Magia aventuras hechizos amistad escuela",
                "Anillos guerra fantasía aventura épica",
                "Familia pueblo generaciones realismo mágico",
                "Romance sociedad amor matrimonio",
                "Gobierno vigilancia distopía política",
                "Caballero aventuras humor clásico",
                "Supervivencia competencia futuro distopía",
                "Dioses mitología aventura fantasía",
                "Dragones aventura fantasía épica",
                "Misterio asesinato drama latinoamericano"
            ]
        }

        return pd.DataFrame(datos)

    # =====================================================
    # CARGAR DATOS
    # =====================================================

    df = cargar_datos()

    # =====================================================
    # MODELO DE RECOMENDACIÓN
    # =====================================================

    # Combinar texto
    df["contenido"] = (
        df["Genero"] + " " +
        df["Descripcion"] + " " +
        df["Autor"]
    )

    # TF-IDF
    vectorizador = TfidfVectorizer()

    matriz_tfidf = vectorizador.fit_transform(df["contenido"])

    # Similaridad
    similitud = cosine_similarity(matriz_tfidf)

    # =====================================================
    # FUNCIÓN RECOMENDAR
    # =====================================================

    def recomendar_libros(titulo, n=5):

        indice = df[df["Titulo"] == titulo].index[0]

        puntajes = list(enumerate(similitud[indice]))

        puntajes = sorted(
            puntajes,
            key=lambda x: x[1],
            reverse=True
        )

        # Eliminar el mismo libro
        puntajes = puntajes[1:n+1]

        recomendaciones = []

        for i in puntajes:

            recomendaciones.append({

                "Título": df.iloc[i[0]]["Titulo"],
                "Autor": df.iloc[i[0]]["Autor"],
                "Género": df.iloc[i[0]]["Genero"],
                "Similitud (%)": round(i[1] * 100, 2)

            })

        return pd.DataFrame(recomendaciones)

    # =====================================================
    # HEADER
    # =====================================================

    st.title("📚 Sistema Inteligente de Recomendación de Libros")

    st.write("""
    Este sistema recomienda libros similares utilizando:

    - Machine Learning
    - TF-IDF
    - Similaridad del coseno
    - Procesamiento de texto

    El objetivo es encontrar libros relacionados
    según género, autor y descripción.
    """)

    st.divider()

    # =====================================================
    # MÉTRICAS
    # =====================================================

    c1, c2, c3 = st.columns(3)

    c1.metric("📚 Libros", len(df))
    c2.metric("✍️ Autores", df["Autor"].nunique())
    c3.metric("🎭 Géneros", df["Genero"].nunique())

    st.divider()

    # =====================================================
    # DATASET
    # =====================================================

    with st.expander("📋 Ver Dataset"):

        st.dataframe(df, use_container_width=True)

    # =====================================================
    # SELECTOR
    # =====================================================

    st.subheader("🔎 Selecciona un libro")

    libro = st.selectbox(
        "Libro",
        df["Titulo"]
    )

    # =====================================================
    # BOTÓN
    # =====================================================

    if st.button("📖 Recomendar Libros"):

        recomendaciones = recomendar_libros(libro)

        st.subheader(f"📚 Libros similares a: {libro}")

        st.dataframe(
            recomendaciones,
            use_container_width=True
        )

        # =================================================
        # GRÁFICO
        # =================================================

        st.subheader("📊 Nivel de similitud")

        fig = px.bar(
            recomendaciones,
            x="Título",
            y="Similitud (%)",
            color="Género",
            title="Similitud entre libros"
        )

        st.plotly_chart(fig, use_container_width=True)

        # =================================================
        # CONCLUSIÓN
        # =================================================

        st.success(f"""
        ✔ El sistema encontró libros similares a "{libro}"
        utilizando algoritmos de Machine Learning.

        Las recomendaciones fueron generadas a partir de:

        - Género
        - Autor
        - Descripción del contenido
        """)

    # =====================================================
    # FOOTER
    # =====================================================

    st.divider()

    st.caption("""
    Sistema desarrollado con:
    Python, Streamlit, Scikit-Learn y Plotly.
    """)

# =========================================================
# EJECUCIÓN
# =========================================================

if __name__ == "__main__":
    sm()