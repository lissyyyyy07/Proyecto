# =========================================================
# IMPORTACIONES
# =========================================================

import streamlit as st
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import pandas as pd
import urllib3

# Evita advertencias SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# =========================================================
# SCRAPING DE OPINIONES
# =========================================================

def scrape_opinions(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10,
            verify=False
        )

        if response.status_code != 200:
            st.error(f"Error HTTP: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        opinions = []

        selectors = [
            ".comment",
            ".comments",
            ".review",
            ".reviews",
            ".opinion",
            ".user-review",
            ".post-content",
            "[id*=comment]",
            "[class*=comment]",
            "[class*=review]"
        ]

        for selector in selectors:

            elements = soup.select(selector)

            for elem in elements:

                text = elem.get_text(" ", strip=True)

                if len(text) > 30:
                    opinions.append(text)

        # Respaldo: usar párrafos
        if not opinions:

            paragraphs = soup.find_all("p")

            opinions = [
                p.get_text().strip()
                for p in paragraphs
                if len(p.get_text().strip()) > 40
            ]

        # Eliminar duplicados
        opinions = list(dict.fromkeys(opinions))

        return opinions

    except Exception as e:
        st.error(f"Error al hacer scraping: {e}")
        return []


# =========================================================
# ANÁLISIS DE SENTIMIENTO
# =========================================================

def get_sentiment(text):

    analysis = TextBlob(text)

    polarity = analysis.sentiment.polarity

    if polarity > 0.1:
        label = "Positivo 😊"
    elif polarity < -0.1:
        label = "Negativo 😡"
    else:
        label = "Neutral 😐"

    return polarity, label


# =========================================================
# FUNCIÓN PRINCIPAL
# =========================================================

def scrapyng():

    st.set_page_config(
        page_title="Análisis de Sentimientos",
        layout="wide"
    )

    st.title("🗣️ Análisis de Sentimientos y Scraping")

    st.markdown("""
    Esta aplicación:

    ✅ Extrae opiniones de una página web  
    ✅ Analiza el sentimiento de cada opinión  
    ✅ Muestra estadísticas y gráficos
    """)

    url = st.text_input(
        "🔗 Ingresa la URL de una noticia, foro, blog o publicación:"
    )

    if st.button("Analizar Opiniones"):

        if not url:
            st.warning("Por favor ingresa una URL.")
            return

        with st.spinner("Extrayendo opiniones..."):

            opinions = scrape_opinions(url)

        if not opinions:
            st.warning("No se encontraron opiniones.")
            return

        results = []

        for opinion in opinions:

            polarity, sentiment = get_sentiment(opinion)

            results.append({
                "Opinión": opinion,
                "Polaridad": round(polarity, 3),
                "Sentimiento": sentiment
            })

        df = pd.DataFrame(results)

        st.subheader("📋 Opiniones Encontradas")
        st.dataframe(df, use_container_width=True)

        positivos = len(
            df[df["Sentimiento"].str.contains("Positivo")]
        )

        negativos = len(
            df[df["Sentimiento"].str.contains("Negativo")]
        )

        neutrales = len(
            df[df["Sentimiento"].str.contains("Neutral")]
        )

        st.subheader("📊 Resumen")

        col1, col2, col3 = st.columns(3)

        col1.metric("Positivas", positivos)
        col2.metric("Negativas", negativos)
        col3.metric("Neutrales", neutrales)

        promedio = df["Polaridad"].mean()

        st.write(
            f"### Polaridad Promedio: {promedio:.3f}"
        )

        if promedio > 0.1:
            st.success("Sentimiento General Positivo 😊")

        elif promedio < -0.1:
            st.error("Sentimiento General Negativo 😡")

        else:
            st.info("Sentimiento General Neutral 😐")

        st.subheader("📈 Distribución de Sentimientos")

        conteo = df["Sentimiento"].value_counts()

        st.bar_chart(conteo)


# =========================================================
# EJECUCIÓN
# =========================================================

if __name__ == "__main__":
    scrapyng()