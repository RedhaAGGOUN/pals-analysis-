import pandas as pd
import os

# 📁 Définir les chemins
data_path = "1_data"
boss_path = os.path.join(data_path, "Palworld_Data-comparison of ordinary BOSS attributes.csv")

# 📥 Chargement des données avec en-tête à la première ligne
df = pd.read_csv(boss_path, header=0)

# 🧹 Nettoyage des données

# 1. Supprimer les colonnes entièrement vides
df = df.dropna(axis=1, how='all')

# 2. Supprimer les colonnes sans nom explicite
df = df.loc[:, ~df.columns.str.contains('^Unnamed', case=False, na=False)]

# 3. Supprimer les doublons
df = df.drop_duplicates()

# 4. Normaliser les noms de colonnes
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(' ', '_')
)

# 🧠 Cas particulier : tout est peut-être regroupé dans une seule colonne → tentative de découpage automatique
if df.shape[1] == 1:
    print("⚠️ Une seule colonne détectée — tentative de restructuration automatique...")
    df = df[df.columns[0]].astype(str).str.split(',', expand=True)
    df.columns = [f"col_{i}" for i in range(df.shape[1])]
    df = df.dropna(how="all")

# 👀 Affichage de l’aperçu
print("✅ ordinary_boss : données nettoyées :")
print(df.head())

# 💾 Export du fichier nettoyé
os.makedirs("2_cleaned", exist_ok=True)
output_path = "2_cleaned/ordinary_boss_clean.csv"
df.to_csv(output_path, index=False)
print(f"📁 Fichier exporté vers : {output_path}")
