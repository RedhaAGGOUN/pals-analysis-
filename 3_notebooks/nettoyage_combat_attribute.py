# 📁 Fichier : 3_notebooks/nettoyage_combat_attribute.py

import pandas as pd
import os

# 🔍 Localisation absolue basée sur le script courant
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "..", "1_data")
output_dir = os.path.join(script_dir, "..", "2_cleaned", "cleaned_palworld_data_Heidi")
input_file = "Palworld_Data--Palu combat attribute table.csv"
output_file = "combat_attribute_clean.csv"

# 📥 Chargement du fichier CSV en texte
df = pd.read_csv(os.path.join(data_dir, input_file), dtype=str, keep_default_na=False)

# 🧹 Nettoyage des colonnes
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df = df.dropna(axis=1, how="all")  # Supprime colonnes vides
df = df.loc[:, ~df.columns.str.contains("^unnamed", case=False)]
df = df.drop_duplicates()

# 🔄 Remplissage des cellules vides
for col in df.columns:
    unique_vals = df[col].dropna().unique()
    clean_vals = set([val.strip().lower() for val in unique_vals if val.strip() != ""])

    if all(val in ["yes", "no"] for val in clean_vals):
        df[col] = df[col].apply(lambda x: x.strip().lower() if x.strip().lower() in ["yes", "no"] else "no")
    elif df[col].str.replace('.', '', 1).str.isnumeric().all():
        df[col] = df[col].replace(r'^\s*$', '0', regex=True)
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    else:
        df[col] = df[col].replace(r'^\s*$', 'n/a', regex=True)

# 💾 Export dans le dossier cible
os.makedirs(output_dir, exist_ok=True)
export_path = os.path.join(output_dir, output_file)
df.to_csv(export_path, index=False, encoding='utf-8')

print(f"✅ Données nettoyées exportées ici : {export_path}")
