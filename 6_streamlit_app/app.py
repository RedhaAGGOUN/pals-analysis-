import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
from mysql.connector import Error

st.set_page_config(page_title="Analyse des Pals", layout="wide")

# ✅ Configuration de la base de données (à personnaliser si besoin)
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",  # 🛠 Mot de passe Heidi confirmé
    "database": "palworld_database"
}

# ✅ Connexion test à la base (optionnelle)
def test_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return True
    except Error:
        return False
    return False

# ✅ Chargement d'une table SQL depuis MariaDB
@st.cache_data
def load_from_db(table_name):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        conn.close()
        return df
    except Error as e:
        st.error(f"Erreur lors de la connexion à la base de données: {e}")
        return pd.DataFrame()

# 🔐 Authentification basique avec gestion de rôle
if "auth" not in st.session_state:
    st.session_state.auth = False
if "user_role" not in st.session_state:
    st.session_state.user_role = ""

if not st.session_state.auth:
    st.title("🔐 Connexion utilisateur")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if username == "admin" and password == "admin":
        st.session_state.auth = True
        st.session_state.user_role = "admin"
        st.success("Connecté comme administrateur")
        st.rerun()
    elif username == "user" and password == "user":
        st.session_state.auth = True
        st.session_state.user_role = "user"
        st.success("Connecté comme utilisateur")
        st.rerun()
    else:
        st.stop()

# 🌐 Navigation principale
page = st.sidebar.radio("Navigation", ["🏠 A propos", "📊 Analyse des données", "📈 Tableau de bord global"])

# 📂 Tables disponibles
TABLES = {
    "🧬 Combat Attribute": "combat_attribute",
    "🔮 Hidden Attribute": "hidden_attribute",
    "⚙️ Job Skill": "job_skill",
    "👹 Ordinary Boss": "ordinary_boss",
    "📈 Refresh Level": "refresh_level",
    "🏯 Tower Boss": "tower_boss"
}

# 🏠 A propos
if page == "🏠 A propos":
    st.title("📚 Projet : Analyse des Pals")
    st.markdown("""
    Ce projet vise à analyser différentes dimensions du jeu **Palworld** à partir de ses données internes :

    - **Attributs de combat des créatures**
    - **Attributs cachés**
    - **Compétences des jobs**
    - **Boss ordinaires et de tours**
    - **Niveaux d’apparition / refresh**
    """)
    if test_db_connection():
        st.success("✅ Connexion à la base MariaDB établie avec succès !")
    else:
        st.error("❌ La connexion à la base a échoué. Vérifiez la configuration.")

# 📈 Tableau de bord global
elif page == "📈 Tableau de bord global":
    st.title("📈 Vue d'ensemble des tables")
    col1, col2 = st.columns(2)
    for label, table in TABLES.items():
        df = load_from_db(table)
        with col1 if list(TABLES.keys()).index(label) % 2 == 0 else col2:
            st.metric(label, f"{len(df)} lignes")

# 📊 Analyse des données
elif page == "📊 Analyse des données":
    st.title("🔍 Analyse des Pals - Application Streamlit")

    selected_label = st.sidebar.selectbox("Choisissez une table :", list(TABLES.keys()))
    selected_table = TABLES[selected_label]
    df = load_from_db(selected_table)

    if df.empty:
        st.stop()

    st.subheader(f"Aperçu de la table : {selected_label}")
    refresh = st.button("🔄 Rafraîchir les données")
    if refresh:
        st.cache_data.clear()
        st.experimental_rerun()

    st.dataframe(df, use_container_width=True)

    st.markdown("### 📊 Statistiques descriptives")
    st.write(df.describe(include='all').transpose())

    if st.checkbox("🔍 Filtrer par colonne"):
        col = st.selectbox("Colonne à filtrer :", df.columns)
        values = df[col].dropna().unique()
        choice = st.selectbox("Valeur :", sorted(values))
        filtered_df = df[df[col] == choice]
        st.success(f"{len(filtered_df)} ligne(s) trouvée(s)")
        st.dataframe(filtered_df, use_container_width=True)
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Télécharger les données filtrées", csv, "filtered_data.csv", "text/csv")

    if st.checkbox("📈 Générer un graphique automatique"):
        num_cols = df.select_dtypes(include=['int64', 'float64']).columns
        if len(num_cols) >= 2:
            x = st.selectbox("Axe X :", num_cols, index=0)
            y = st.selectbox("Axe Y :", num_cols, index=1)
            plt.figure(figsize=(10, 5))
            sns.scatterplot(data=df, x=x, y=y)
            st.pyplot(plt)

    # Mode admin
    if st.session_state.user_role == "admin" and st.sidebar.checkbox("🛡️ Mode Admin"):
        st.markdown("### ➕ Ajouter une ligne")
        with st.form("ajout_form"):
            new_data = {col: st.text_input(col) for col in df.columns}
            if st.form_submit_button("Ajouter"):
                try:
                    conn = mysql.connector.connect(**DB_CONFIG)
                    cursor = conn.cursor()
                    cols = ", ".join(new_data.keys())
                    vals = ", ".join([f"'{v}'" for v in new_data.values()])
                    cursor.execute(f"INSERT INTO {selected_table} ({cols}) VALUES ({vals})")
                    conn.commit()
                    conn.close()
                    st.success("Donnée ajoutée !")
                except Error as e:
                    st.error(f"Erreur SQL : {e}")

        st.markdown("### ❌ Supprimer une ligne par ID")
        del_id = st.text_input("ID à supprimer")
        if st.button("Supprimer"):
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor()
                cursor.execute(f"DELETE FROM {selected_table} WHERE id = {del_id}")
                conn.commit()
                conn.close()
                st.warning(f"ID {del_id} supprimé")
            except Error as e:
                st.error(f"Erreur : {e}")

    st.sidebar.markdown("---")
    st.sidebar.markdown("📬 Feedback utilisateur")
    feedback = st.sidebar.text_area("Votre message")
    if st.sidebar.button("Envoyer"):
        st.sidebar.success("Merci pour votre retour !")
