import streamlit as st
import pandas as pd
import mysql.connector
import seaborn as sns
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Palworld Analyse Pro", layout="wide")
st.title("🐉 Analyse Avancée des Données Palworld")

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "palworld_database",
}

@st.cache_data(ttl=3600)
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

st.sidebar.header("🔎 Navigation")
selected_table_key = st.sidebar.selectbox("Choisissez une table", list(TABLES.keys()), format_func=lambda x: TABLES[x])
df = load_from_db(selected_table_key)

if df is None:
    st.error("Impossible de charger les données depuis la base.")
    st.stop()

st.success(f"{len(df)} lignes chargées pour la table : {TABLES[selected_table_key]}")

# Aperçu des données
with st.expander("👁️ Aperçu des données"):
    st.dataframe(df, use_container_width=True)

# Filtres dynamiques
st.sidebar.subheader("🎛️ Filtres dynamiques")
for col in df.select_dtypes(include=["object", "category"]).columns:
    valeurs = df[col].dropna().unique().tolist()
    choix = st.sidebar.multiselect(f"Filtrer {col}", valeurs)
    if choix:
        df = df[df[col].isin(choix)]

# Statistiques
with st.expander("📈 Statistiques descriptives"):
    st.dataframe(df.describe(), use_container_width=True)

# Visualisation
st.header("📊 Visualisation des données")
numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

if numeric_cols:
    col1, col2, col3 = st.columns(3)
    with col1:
        x_axis = st.selectbox("Axe X", numeric_cols)
    with col2:
        y_axis = st.selectbox("Axe Y (facultatif)", [None] + numeric_cols)
    with col3:
        graph_type = st.selectbox("Type de graphique", ["Histogramme", "Nuage de points", "Boxplot", "Heatmap"])

    fig, ax = plt.subplots(figsize=(10, 5))

    if graph_type == "Histogramme":
        sns.histplot(df[x_axis], kde=True, ax=ax)
    elif graph_type == "Nuage de points" and y_axis:
        sns.scatterplot(data=df, x=x_axis, y=y_axis, ax=ax)
    elif graph_type == "Boxplot" and y_axis:
        sns.boxplot(data=df, x=x_axis, y=y_axis, ax=ax)
    elif graph_type == "Heatmap":
        corr = df[numeric_cols].corr()
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)

    st.pyplot(fig)

    # Export PNG
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    st.download_button("🔍 Télécharger le graphique", buf.getvalue(), file_name="graphique_palworld.png")
else:
    st.warning("Aucune colonne numérique à visualiser.")

# Export CSV
st.download_button("📂 Télécharger les données filtrées", df.to_csv(index=False).encode("utf-8"), file_name=f"{selected_table_key}_filtre.csv")
