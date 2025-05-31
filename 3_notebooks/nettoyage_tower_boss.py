import pandas as pd
import os

# 📁 Définir les chemins
data_path = "1_data"
tower_path = os.path.join(data_path, "Palworld_Data-Tower BOSS attribute comparison.csv")

# 📥 Chargement des données avec en-tête sur la première ligne
df = pd.read_csv(tower_path, header=0)

# 🧹 Étapes de nettoyage

# 1. Supprimer les colonnes totalement vides
df = df.dropna(axis=1, how='all')

# 2. Supprimer les colonnes sans nom (souvent générées automatiquement : "Unnamed")
df = df.loc[:, ~df.columns.str.contains('^Unnamed', case=False, na=False)]

# 3. Supprimer les doublons éventuels
df = df.drop_duplicates()

# 4. Nettoyer les noms de colonnes (minuscules, sans espaces)
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(' ', '_')
)

# 👀 Aperçu rapide
print("✅ tower_boss : données nettoyées :")
print(df.head())

# 💾 Sauvegarde dans le dossier de sortie
os.makedirs("2_cleaned", exist_ok=True)
output_path = "2_cleaned/tower_boss_clean.csv"
df.to_csv(output_path, index=False)
print(f"📁 Fichier exporté vers : {output_path}")
