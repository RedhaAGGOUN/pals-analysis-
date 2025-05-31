import pandas as pd
import os

# 📁 Définir les chemins
data_path = "1_data"
refresh_path = os.path.join(data_path, "Palworld_Data--Palu refresh level.csv")

# 📥 Chargement des données avec l'en-tête à la première ligne
df = pd.read_csv(refresh_path, header=0)

# 🧹 Nettoyage des données

# 1. Supprimer les colonnes totalement vides
df = df.dropna(axis=1, how='all')

# 2. Supprimer les colonnes sans nom explicite (ex : "Unnamed: x")
df = df.loc[:, ~df.columns.str.contains('^Unnamed', case=False, na=False)]

# 3. Supprimer les doublons éventuels
df = df.drop_duplicates()

# 4. Nettoyer les noms de colonnes : minuscules, sans espace
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(' ', '_')
)

# 🧠 Si une seule colonne, tenter une restructuration automatique (découpage par virgule)
if df.shape[1] == 1:
    print("⚠️ Une seule colonne détectée — tentative de restructuration automatique...")
    df = df[df.columns[0]].astype(str).str.split(',', expand=True)
    df.columns = [f"col_{i}" for i in range(df.shape[1])]
    df = df.dropna(how="all")

# 👀 Aperçu
print("✅ refresh_level : données nettoyées :")
print(df.head())

# 💾 Export du fichier nettoyé
os.makedirs("2_cleaned", exist_ok=True)
output_path = "2_cleaned/refresh_level_clean.csv"
df.to_csv(output_path, index=False)
print(f"📁 Fichier exporté vers : {output_path}")
