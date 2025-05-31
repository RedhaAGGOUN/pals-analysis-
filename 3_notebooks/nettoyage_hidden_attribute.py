import pandas as pd
import os

# 📁 Définir le chemin vers le dossier contenant les données
data_path = "1_data"
hidden_path = os.path.join(data_path, "Palworld_Data-hide pallu attributes.csv")

# 📥 Chargement du fichier avec en-tête à la première ligne
df = pd.read_csv(hidden_path, header=0)

# 🧹 Étapes de nettoyage

# 1. Supprimer les colonnes entièrement vides (souvent dues à un mauvais encodage ou des exports incomplets)
df = df.dropna(axis=1, how='all')

# 2. Supprimer les colonnes sans nom explicite (généralement nommées "Unnamed: x" automatiquement)
df = df.loc[:, ~df.columns.str.contains('^Unnamed', case=False, na=False)]

# 3. Supprimer les doublons parmi les lignes (utile si le fichier a été fusionné plusieurs fois)
df = df.drop_duplicates()

# 4. Nettoyer les noms de colonnes : enlever les espaces, passer en minuscules, remplacer les espaces par des "_"
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(' ', '_')
)

# 👀 Affichage d’un aperçu des premières lignes
print("✅ hidden_attribute : données nettoyées :")
print(df.head())

# 💾 Export du fichier nettoyé dans le dossier de sortie
os.makedirs("2_cleaned", exist_ok=True)
output_path = "2_cleaned/hidden_attribute_clean.csv"
df.to_csv(output_path, index=False)
print(f"📁 Fichier exporté vers : {output_path}")
