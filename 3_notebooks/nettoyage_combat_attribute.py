import pandas as pd
import os

# 📁 Chemin vers le fichier source
data_path = "1_data"
combat_path = os.path.join(data_path, "Palworld_Data--Palu combat attribute table.csv")

# 📥 Chargement des données avec en-tête à la première ligne (corrigé ici : header=0)
combat_df = pd.read_csv(combat_path, header=0)

# 🧹 Nettoyage des données

# 1. Supprimer les colonnes entièrement vides
combat_df = combat_df.dropna(axis=1, how='all')

# 2. Supprimer les colonnes sans nom explicite (souvent générées automatiquement : "Unnamed")
combat_df = combat_df.loc[:, ~combat_df.columns.str.contains('^Unnamed', case=False, na=False)]

# 3. Supprimer les doublons éventuels dans les lignes
combat_df = combat_df.drop_duplicates()

# 4. Normaliser les noms de colonnes (minuscules, sans espaces)
combat_df.columns = (
    combat_df.columns
    .str.strip()
    .str.lower()
    .str.replace(' ', '_')
)

# 👀 Affichage d’un aperçu des données nettoyées
print("✅ Données 'combat_attribute' nettoyées :")
print(combat_df.head())

# 💾 Sauvegarde du fichier nettoyé dans le dossier de sortie
output_path = "2_cleaned/combat_attribute_clean.csv"
os.makedirs("2_cleaned", exist_ok=True)
combat_df.to_csv(output_path, index=False)
print(f"📁 Fichier exporté vers : {output_path}")
