import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================
# CONFIGURACIÓN
# =========================================

st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================================
# CACHE DATA
# =========================================

@st.cache_data
def cargar_datos():
    return pd.read_csv("datos.csv")

# =========================================
# ESTILOS
# =========================================

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

# =========================================
# DESCRIPCIÓN CAMPOS
# =========================================

descripciones = {

    "Order Date": "Fecha de la orden.",

    "Product Name": "Nombre del producto.",

    "Category": "Categoría del producto.",

    "Region": "Región de venta.",

    "Quantity": "Cantidad vendida.",

    "Sales": "Ventas totales.",

    "Profit": "Ganancia obtenida."
}

# =========================================
# APP
# =========================================

def eda():

    # =====================================
    # DATASET
    # =====================================

    df = cargar_datos()

    # =====================================
    # LIMPIAR COLUMNAS
    # =====================================

    df.columns = df.columns.str.strip()

    # =====================================
    # HEADER
    # =====================================

    st.title("📊 E-Commerce Dashboard")

    st.write("""
    Dashboard interactivo de análisis exploratorio.
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
    # MENÚ
    # =====================================

    col1, col2 = st.columns([1, 2])

    with col1:

        opcion = st.radio(
            "📌 Menú",
            [
                "📋 Primeras filas",
                "📏 Dimensiones",
                "🧩 Tipos de datos",
                "📈 Estadísticas",
                "📝 Descripción de campos",
                "🧭 Navegador dataset",
                "🔎 Buscador",
                "📊 Gráficos",
                "🧪 Hipótesis"
            ]
        )

    with col2:

        # =================================
        # PRIMERAS FILAS
        # =================================

        if opcion == "📋 Primeras filas":

            st.subheader("📋 Dataset")

            st.dataframe(
                df.head(),
                use_container_width=True
            )

        # =================================
        # DIMENSIONES
        # =================================

        elif opcion == "📏 Dimensiones":

            filas, columnas = df.shape

            a, b = st.columns(2)

            a.metric("Filas", filas)

            b.metric("Columnas", columnas)

        # =================================
        # TIPOS DE DATOS
        # =================================

        elif opcion == "🧩 Tipos de datos":

            tipos = pd.DataFrame({

                "Columna": df.columns,

                "Tipo": df.dtypes.values

            })

            st.dataframe(
                tipos,
                use_container_width=True
            )

        # =================================
        # ESTADÍSTICAS
        # =================================

        elif opcion == "📈 Estadísticas":

            st.subheader("📈 Estadísticas")

            st.dataframe(
                df.describe(),
                use_container_width=True
            )

        # =================================
        # DESCRIPCIÓN DE CAMPOS
        # =================================

        elif opcion == "📝 Descripción de campos":

            st.subheader("📝 Descripción de Campos")

            campo = st.selectbox(
                "Seleccione un campo",
                df.columns
            )

            st.success(
                descripciones.get(
                    campo,
                    "Sin descripción"
                )
            )

            # NUMÉRICO
            if pd.api.types.is_numeric_dtype(df[campo]):

                st.write("### 📈 Estadísticas")

                st.dataframe(
                    df[campo].describe(),
                    use_container_width=True
                )

            # CATEGÓRICO
            else:

                st.write("### 🧩 Valores posibles")

                valores = pd.DataFrame({

                    "Valores":
                    df[campo].unique()

                })

                st.dataframe(
                    valores,
                    use_container_width=True
                )

        # =================================
        # NAVEGADOR DATASET
        # =================================

        elif opcion == "🧭 Navegador dataset":

            st.subheader("🧭 Navegador Dataset")

            inicio = st.number_input(
                "Fila inicial",
                0,
                len(df)-1,
                0
            )

            fin = st.number_input(
                "Fila final",
                1,
                len(df),
                20
            )

            st.dataframe(
                df.iloc[inicio:fin],
                use_container_width=True
            )

        # =================================
        # BUSCADOR
        # =================================

        elif opcion == "🔎 Buscador":

            st.subheader("🔎 Buscador de registros")

            columna_busqueda = st.selectbox(
                "Selecciona columna",
                df.columns
            )

            valor = st.text_input("Ingresa valor a buscar")

            if valor:

                resultado = df[
                    df[columna_busqueda]
                    .astype(str)
                    .str.contains(valor, case=False, na=False)
                ]

                st.write(f"Resultados encontrados: {len(resultado)}")

                st.dataframe(resultado, use_container_width=True)

        # =================================
        # GRÁFICOS OPTIMIZADOS
        # =================================

        elif opcion == "📊 Gráficos":

            st.subheader("📊 Graficador Exploratorio")

            campo = st.selectbox(
                "Seleccione un campo",
                df.columns
            )

            # =================================
            # CAMPOS NUMÉRICOS
            # =================================

            if pd.api.types.is_numeric_dtype(df[campo]):

                tipo_grafico = st.selectbox(
                    "Tipo de gráfico",
                    [
                        "Histograma",
                        "Boxplot"
                    ]
                )

                # HISTOGRAMA
                if tipo_grafico == "Histograma":

                    fig = px.histogram(
                        df,
                        x=campo,
                        nbins=20,
                        title=f"Distribución de {campo}",
                        template="plotly_dark"
                    )

                # BOXPLOT
                else:

                    fig = px.box(
                        df,
                        y=campo,
                        title=f"Boxplot de {campo}",
                        template="plotly_dark"
                    )

            # =================================
            # CAMPOS CATEGÓRICOS
            # =================================

            else:

                # SOLO TOP 10 VALORES
                datos = (
                    df[campo]
                    .value_counts()
                    .head(10)
                    .reset_index()
                )

                datos.columns = [campo, "Cantidad"]

                fig = px.bar(
                    datos,
                    x=campo,
                    y="Cantidad",
                    color="Cantidad",
                    title=f"Top 10 valores de {campo}",
                    template="plotly_dark"
                )

            # =================================
            # OPTIMIZACIÓN
            # =================================

            fig.update_layout(
                height=500,
                xaxis_tickangle=-45
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # =================================
        # HIPÓTESIS
        # =================================

        elif opcion == "🧪 Hipótesis":

            st.subheader("🧪 Hipótesis")

            hipotesis = st.selectbox(
                "Seleccione hipótesis",
                [
                    "Más ventas generan más profit",
                    "Las regiones tienen diferentes niveles de ventas"
                ]
            )

            # =================================
            # HIPÓTESIS 1
            # =================================

            if hipotesis == "Más ventas generan más profit":

                fig = px.scatter(
                    df,
                    x="Sales",
                    y="Profit",
                    color="Category",
                    title="Sales vs Profit",
                    template="plotly_dark"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                correlacion = df["Sales"].corr(
                    df["Profit"]
                )

                st.metric(
                    "Correlación",
                    f"{correlacion:.2f}"
                )

                st.success("""
                Existe una relación positiva entre
                ventas y profit.
                """)

            # =================================
            # HIPÓTESIS 2
            # =================================

            else:

                datos = (
                    df.groupby("Region")["Sales"]
                    .sum()
                    .reset_index()
                )

                fig = px.bar(
                    datos,
                    x="Region",
                    y="Sales",
                    color="Region",
                    title="Ventas por Región",
                    template="plotly_dark"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                st.success("""
                Existen diferencias importantes
                entre regiones.
                """)

# =========================================
# EJECUTAR
# =========================================

if __name__ == "__main__":

    eda()

