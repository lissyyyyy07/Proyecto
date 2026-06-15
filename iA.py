# =========================================
# IMPORTACIONES
# =========================================

import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================
# CONFIGURACIÓN
# =========================================

st.set_page_config(
    page_title="AI Dataset Assistant",
    page_icon="🤖",
    layout="wide"
)

# =========================================
# ESTILOS
# =========================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg,#0F172A,#111827,#1E293B);
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
    border-radius: 18px;
    padding: 18px;
    border: 1px solid #334155;
}

.stTextInput > div > div > input {
    background-color: #1E293B;
    color: white;
    border: 1px solid #38BDF8;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# CARGAR DATASET
# =========================================

@st.cache_data
def cargar_datos():

    df = pd.read_csv("datos.csv")

    df.columns = df.columns.str.strip()

    return df

# =========================================
# NORMALIZAR TEXTO
# =========================================

def limpiar_texto(texto):

    texto = texto.lower()

    reemplazos = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u"
    }

    for k, v in reemplazos.items():
        texto = texto.replace(k, v)

    return texto

# =========================================
# IA DATASET
# =========================================

def iA():

    # =====================================
    # DATASET
    # =====================================

    df = cargar_datos()

    # =====================================
    # HEADER
    # =====================================

    st.title("🤖 AI E-Commerce Assistant")

    st.write("""
    Consulta libremente tu dataset usando lenguaje natural.
    """)

    st.divider()

    # =====================================
    # MÉTRICAS
    # =====================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "💰 Ventas Totales",
        f"${df['Sales'].sum():,.0f}"
    )

    c2.metric(
        "📈 Profit Total",
        f"${df['Profit'].sum():,.0f}"
    )

    c3.metric(
        "📦 Productos",
        df['Product Name'].nunique()
    )

    c4.metric(
        "🌍 Regiones",
        df['Region'].nunique()
    )

    st.divider()

    # =====================================
    # SIDEBAR
    # =====================================

    st.sidebar.title("🤖 Consultas Inteligentes")

    st.sidebar.info("""
    Ejemplos:

    • ¿Qué categoría vende más?
    • ¿Cuál región tiene más profit?
    • Muéstrame los top productos
    • ¿Cuánto es el promedio de ventas?
    • ¿Qué producto genera más ganancias?
    • Mostrar dataset
    • Primeras filas
    • Top regiones
    • Top categorías
    • Productos con más profit
    """)

    # =====================================
    # PROMPT ABIERTO
    # =====================================

    prompt = st.text_input(
        "💬 Pregunta lo que quieras sobre el dataset"
    )

    if prompt:

        pregunta = limpiar_texto(prompt)

        # =================================
        # CATEGORÍAS MÁS VENTAS
        # =================================

        if (
            "categoria" in pregunta
            and
            (
                "vende" in pregunta
                or
                "ventas" in pregunta
            )
        ):

            datos = (
                df.groupby("Category")["Sales"]
                .sum()
                .sort_values(ascending=False)
            )

            st.success(
                f"🏆 La categoría con más ventas es: {datos.index[0]}"
            )

            fig = px.bar(
                datos,
                title="Ventas por Categoría",
                template="plotly_dark"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # =================================
        # REGIÓN MÁS PROFIT
        # =================================

        elif (
            "region" in pregunta
            and
            "profit" in pregunta
        ):

            datos = (
                df.groupby("Region")["Profit"]
                .sum()
                .sort_values(ascending=False)
            )

            st.success(
                f"🌍 La región con mayor profit es: {datos.index[0]}"
            )

            fig = px.pie(
                values=datos.values,
                names=datos.index,
                title="Profit por Región",
                template="plotly_dark"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # =================================
        # TOP PRODUCTOS
        # =================================

        elif (
            "top productos" in pregunta
            or
            "productos" in pregunta
            or
            "mas vendidos" in pregunta
        ):

            datos = (
                df.groupby("Product Name")["Sales"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
            )

            st.write("## 🏆 Top Productos")

            st.dataframe(datos)

            fig = px.bar(
                datos,
                title="Top Productos",
                template="plotly_dark"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # =================================
        # PROMEDIO VENTAS
        # =================================

        elif (
            "promedio" in pregunta
            and
            "ventas" in pregunta
        ):

            promedio = df["Sales"].mean()

            st.metric(
                "📊 Promedio de Ventas",
                f"${promedio:,.2f}"
            )

        # =================================
        # PROMEDIO PROFIT
        # =================================

        elif (
            "promedio" in pregunta
            and
            "profit" in pregunta
        ):

            promedio = df["Profit"].mean()

            st.metric(
                "📈 Promedio Profit",
                f"${promedio:,.2f}"
            )

        # =================================
        # TOTAL VENTAS
        # =================================

        elif (
            "total ventas" in pregunta
            or
            "ventas totales" in pregunta
        ):

            total = df["Sales"].sum()

            st.metric(
                "💰 Total Ventas",
                f"${total:,.2f}"
            )

        # =================================
        # TOTAL PROFIT
        # =================================

        elif (
            "profit total" in pregunta
            or
            "total profit" in pregunta
        ):

            total = df["Profit"].sum()

            st.metric(
                "📈 Total Profit",
                f"${total:,.2f}"
            )

        # =================================
        # PRODUCTO MÁS VENDIDO
        # =================================

        elif (
            "producto" in pregunta
            and
            "vendido" in pregunta
        ):

            datos = (
                df.groupby("Product Name")["Sales"]
                .sum()
                .sort_values(ascending=False)
            )

            st.success(
                f"🏆 Producto más vendido: {datos.index[0]}"
            )

        # =================================
        # PRODUCTO MÁS PROFIT
        # =================================

        elif (
            "producto" in pregunta
            and
            "profit" in pregunta
        ):

            datos = (
                df.groupby("Product Name")["Profit"]
                .sum()
                .sort_values(ascending=False)
            )

            st.success(
                f"💰 Producto con más profit: {datos.index[0]}"
            )

        # =================================
        # TOP REGIONES
        # =================================

        elif "top regiones" in pregunta:

            datos = (
                df.groupby("Region")["Sales"]
                .sum()
                .sort_values(ascending=False)
            )

            st.dataframe(datos)

            fig = px.bar(
                datos,
                title="Top Regiones",
                template="plotly_dark"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # =================================
        # TOP CATEGORÍAS
        # =================================

        elif "top categorias" in pregunta:

            datos = (
                df.groupby("Category")["Sales"]
                .sum()
                .sort_values(ascending=False)
            )

            st.dataframe(datos)

            fig = px.bar(
                datos,
                title="Top Categorías",
                template="plotly_dark"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # =================================
        # MOSTRAR DATASET
        # =================================

        elif "dataset" in pregunta:

            st.dataframe(
                df,
                use_container_width=True
            )

        # =================================
        # PRIMERAS FILAS
        # =================================

        elif "primeras filas" in pregunta:

            st.dataframe(
                df.head(),
                use_container_width=True
            )

        # =================================
        # COLUMNAS
        # =================================

        elif (
            "columnas" in pregunta
            or
            "campos" in pregunta
        ):

            columnas = pd.DataFrame({
                "Columnas": df.columns
            })

            st.dataframe(
                columnas,
                use_container_width=True
            )

        # =================================
        # DESCRIBE
        # =================================

        elif (
            "estadisticas" in pregunta
            or
            "describe" in pregunta
        ):

            st.dataframe(
                df.describe(),
                use_container_width=True
            )

        # =================================
        # NO ENTENDIÓ
        # =================================

        else:

            st.warning("""
            ❌ No pude interpretar tu consulta.

            Intenta preguntas como:

            • ¿Qué categoría vende más?
            • ¿Cuál región tiene más profit?
            • Top productos
            • Promedio ventas
            • Profit total
            • Mostrar dataset
            """)

# =========================================
# EJECUTAR
# =========================================

if __name__ == "__main__":

    iA()

