
import streamlit as st
import pandas as pd
import mysql.connector
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analyse Palworld", layout="wide")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choisissez une page", ["🏠 Accueil", "📂 Tables", "📊 Figures d'analyse"])

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "palworld_database",
}

@st.cache_data(show_spinner=False)
def load_from_db(table_name):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        conn.close()
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        return df
    except Exception as e:
        return None

TABLES = {
    "combat_attribute_clean": "Attributs de Combat",
    "hidden_attribute_clean": "Attributs Cachés",
    "job_skill_clean": "Compétences de Travail",
    "ordinary_boss_clean": "Boss Ordinaires",
    "refresh_level_clean": "Niveaux de Refresh",
    "tower_boss_clean": "Boss de Tour",
}

if page == "🏠 Accueil":
    st.title("📊 Analyse des Données Palworld")
    st.write("Bienvenue sur l'application d'analyse interactive. Sélectionnez une table ou une figure.")
elif page == "📂 Tables":
    st.title("📂 Aperçu des Tables SQL")
    for table_name, label in TABLES.items():
        df = load_from_db(table_name)
        if df is not None:
            with st.expander(f"{label} ({len(df)} lignes)"):
                st.dataframe(df.head(50), use_container_width=True)
        else:
            st.error(f"❌ Impossible de charger la table : {table_name}")
elif page == "📊 Figures d'analyse":
    st.title("📊 Visualisations personnalisées")
    table_choice = st.selectbox("Sélectionnez une table à analyser", list(TABLES.keys()))
    df = load_from_db(table_choice)
    if df is None:
        st.error("❌ Impossible de charger les données.")
    else:
        st.success(f"{len(df)} lignes chargées.")
        numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
        if not numeric_cols:
            st.warning("Aucune colonne numérique à afficher.")
        else:
            col1, col2 = st.columns(2)
            with col1:
                x_axis = st.selectbox("🧭 Axe X", numeric_cols)
            with col2:
                y_axis = st.selectbox("🧮 Axe Y (facultatif)", [None] + numeric_cols)
            st.subheader("📈 Visualisation")
            plt.figure(figsize=(10, 4))
            if y_axis and y_axis != x_axis:
                sns.scatterplot(data=df, x=x_axis, y=y_axis)
            else:
                sns.histplot(df[x_axis], kde=True)
            st.pyplot(plt)
