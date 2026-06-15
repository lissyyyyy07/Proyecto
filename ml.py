# =========================================
# IMPORTACIONES
# =========================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor, plot_tree, export_text

from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error
)

# =========================================
# CONFIGURACIÓN
# =========================================

st.set_page_config(
    page_title="Machine Learning Dashboard",
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

h1 { color: #38BDF8; font-size: 40px; }

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
# CARGA DATASET
# =========================================

@st.cache_data
def cargar_datos():
    return pd.read_csv("datos.csv")

df = cargar_datos()

# limpiar columnas
df.columns = df.columns.str.strip()

# =========================================
# FUNCIÓN REGLAS ÁRBOL (DINÁMICA)
# =========================================

def mostrar_reglas_arbol(modelo, variables_x):
    reglas = export_text(
        modelo,
        feature_names=list(variables_x)
    )

    st.subheader("🌳 Reglas del Árbol de Decisión (Dinámico)")
    st.code(reglas, language="text")

# =========================================
# APP
# =========================================

def ml():

    st.title("🤖 Machine Learning Dashboard")

    st.write("Modelos interactivos con Streamlit")

    # =====================================
    # SIDEBAR
    # =====================================

    st.sidebar.header("⚙️ Configuración")

    algoritmo = st.sidebar.selectbox(
        "Modelo",
        ["Regresión Lineal", "Árbol de Decisión"]
    )

    # variables numéricas
    num_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    variable_y = st.sidebar.selectbox(
        "🎯 Variable dependiente",
        num_cols
    )

    variables_x = st.sidebar.multiselect(
        "📌 Variables independientes",
        [c for c in num_cols if c != variable_y],
        default=[c for c in num_cols if c != variable_y][:1]
    )

    if len(variables_x) == 0:
        st.warning("Selecciona al menos una variable independiente")
        return

    train_pct = st.sidebar.slider(
        "📊 Train (%)",
        50, 90, 80
    )

    test_size = (100 - train_pct) / 100

    # =====================================
    # DATA
    # =====================================

    X = df[variables_x]
    y = df[variable_y]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=42
    )

    # =====================================
    # MODELO
    # =====================================

    if algoritmo == "Regresión Lineal":
        model = LinearRegression()
    else:
        model = DecisionTreeRegressor(
            max_depth=4,
            random_state=42
        )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_train_pred = model.predict(X_train)

    # =====================================
    # MÉTRICAS
    # =====================================

    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)

    st.subheader("📊 Métricas")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Train %", f"{train_pct}%")
    c2.metric("Test %", f"{100-train_pct}%")
    c3.metric("R²", round(r2, 3))
    c4.metric("MAE", round(mae, 2))

    st.metric("MSE", round(mse, 2))

    # =====================================
    # PREDICCIÓN MANUAL
    # =====================================

    st.subheader("🔮 Predicción manual")

    inputs = []
    cols = st.columns(len(variables_x))

    for i, col in enumerate(variables_x):
        val = cols[i].number_input(col, float(df[col].mean()))
        inputs.append(val)

    pred = model.predict([inputs])[0]

    st.success(f"Predicción: {pred:.2f}")

    # =====================================
    # REGRESIÓN LINEAL (GRÁFICO)
    # =====================================

    if algoritmo == "Regresión Lineal":

        st.subheader("📈 Gráfico Real vs Predicción")

        fig, ax = plt.subplots()

        ax.scatter(y_test, y_pred, label="Test")
        ax.scatter(y_train, y_train_pred, label="Train")

        min_v = min(y_test.min(), y_pred.min())
        max_v = max(y_test.max(), y_pred.max())

        ax.plot([min_v, max_v], [min_v, max_v], "--")

        ax.set_xlabel("Real")
        ax.set_ylabel("Predicción")
        ax.legend()

        st.pyplot(fig)

    # =====================================
    # ÁRBOL (SOLO VISUAL)
    # =====================================

    if algoritmo == "Árbol de Decisión":

        st.subheader("🌳 Árbol de Decisión")

        fig, ax = plt.subplots(figsize=(20, 10))

        plot_tree(
            model,
            feature_names=variables_x,
            filled=True,
            ax=ax
        )

        st.pyplot(fig)

        # 🔥 REGLAS DINÁMICAS (IMPORTANTE)
        mostrar_reglas_arbol(model, variables_x)

# =========================================
# EJECUTAR
# =========================================

if __name__ == "__main__":
    ml()