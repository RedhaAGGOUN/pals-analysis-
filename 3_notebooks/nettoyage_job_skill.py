import pandas as pd
import os

# 📁 Définir les chemins
data_path = "1_data"
job_skill_path = os.path.join(data_path, "Palworld_Data-Palu Job Skills Table.csv")

# 📥 Lecture du fichier avec en-tête sur la première ligne
df = pd.read_csv(job_skill_path, header=0)

# 🧹 Nettoyage des données

# 1. Supprimer les colonnes entièrement vides
df = df.dropna(axis=1, how='all')

# 2. Supprimer les colonnes sans nom explicite (typiquement "Unnamed: x")
df = df.loc[:, ~df.columns.str.contains('^Unnamed', case=False, na=False)]

# 3. Supprimer les doublons éventuels
df = df.drop_duplicates()

# 4. Normalisation des noms de colonnes
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(' ', '_')
)

# 🧠 Cas particulier : si tout est dans une seule colonne, on tente de la découper automatiquement
if df.shape[1] == 1:
    print("⚠️ Une seule colonne détectée — tentative de découpage automatique...")
    col = df.columns[0]
    df = df[col].astype(str).str.split(',', expand=True)
    df.columns = [f"col_{i}" for i in range(df.shape[1])]
    df = df.dropna(how="all")

# 👀 Aperçu des données nettoyées
print("✅ job_skill : données nettoyées :")
print(df.head())

# 💾 Export dans le dossier prévu
os.makedirs("2_cleaned", exist_ok=True)
output_path = "2_cleaned/job_skill_clean.csv"
df.to_csv(output_path, index=False)
print(f"📁 Fichier exporté vers : {output_path}")
