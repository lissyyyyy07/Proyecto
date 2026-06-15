import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
 
 
# ==========================================
# FUNCIÓN PARA DETECTAR EL TIPO DE GRÁFICO
# ==========================================
 
def generar_grafico(df, columna):
 
    fig, ax = plt.subplots(figsize=(8, 5))
 
    # --------------------------------------
    # SI LA COLUMNA ES NUMÉRICA
    # --------------------------------------
 
    if pd.api.types.is_numeric_dtype(df[columna]):
 
        # Pocos valores → barras
        if df[columna].nunique() <= 10:
 
            conteo = df[columna].value_counts()
 
            ax.bar(
                conteo.index.astype(str),
                conteo.values
            )
 
            ax.set_title(f"Gráfico de Barras - {columna}")
 
        # Muchos valores → línea
        else:
 
            ax.plot(
                df[columna],
                marker="o"
            )
 
            ax.set_title(f"Gráfico de Línea - {columna}")
 
    # --------------------------------------
    # SI LA COLUMNA ES CATEGÓRICA
    # --------------------------------------
 
    else:
 
        conteo = df[columna].value_counts()
 
        # Donut chart
        wedges, texts, autotexts = ax.pie(
            conteo.values,
            labels=conteo.index.astype(str),
            autopct="%1.1f%%"
        )
 
        # Crear efecto donut
        centro = plt.Circle((0, 0), 0.60, fc='white')
        fig.gca().add_artist(centro)
 
        ax.set_title(f"Gráfico Donut - {columna}")
 
    st.pyplot(fig)
 
 
# ==========================================
# FUNCIÓN PRINCIPAL
# ==========================================
 
def csvj():
 
    st.title("📊 Visualizador Inteligente de Datos")
 
    st.write(
        "Cargue un archivo CSV o Excel y genere gráficos automáticamente."
    )
 
    # --------------------------------------
    # CARGAR ARCHIVO
    # --------------------------------------
 
    archivo = st.file_uploader(
        "Seleccione un archivo",
        type=["csv", "xlsx", "xls"]
    )
 
    # --------------------------------------
    # SI HAY ARCHIVO
    # --------------------------------------
 
    if archivo is not None:
 
        try:
 
            # Leer CSV
            if archivo.name.endswith(".csv"):
                df = pd.read_csv(archivo)
 
            # Leer Excel
            else:
                df = pd.read_excel(archivo)
 
            # Mostrar datos
            st.subheader("📄 Datos cargados")
            st.dataframe(df)
 
            # Seleccionar columna
            columnas = df.columns.tolist()
 
            st.subheader("⚙️ Seleccione una columna")
 
            columna = st.selectbox(
                "Columna",
                columnas
            )
 
            # ----------------------------------
            # GENERAR GRÁFICO AUTOMÁTICO
            # ----------------------------------
 
            if st.button("Generar gráfico"):
 
                generar_grafico(df, columna)
 
        except Exception as e:
 
            st.error(f"Error: {e}")
 
 
# ==========================================
# EJECUTAR
# ==========================================
 
if __name__ == "__main__":
    csvj()

