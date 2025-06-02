import pandas as pd
import os

# 📂 Chemins dynamiques
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "..", "1_data")
output_dir = os.path.join(script_dir, "..", "2_cleaned", "cleaned_palworld_data_Heidi")

input_file = "Palworld_Data-Palu Job Skills Table.csv"
output_file = "job_skill_clean_fixed.csv"
input_path = os.path.join(data_dir, input_file)
output_path = os.path.join(output_dir, output_file)

# 📥 Chargement des données
df = pd.read_csv(input_path, header=0, dtype=str, keep_default_na=False)

# 🧹 Nettoyage général
df = df.dropna(axis=1, how='all')
df = df.loc[:, ~df.columns.str.contains('^Unnamed', case=False, na=False)]
df = df.drop_duplicates()
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# ⚠️ Cas d'erreur d'encodage ou mauvaise virgule (1 colonne détectée)
if df.shape[1] == 1:
    print("⚠️ Une seule colonne détectée — tentative de découpage automatique...")
    col = df.columns[0]
    df = df[col].astype(str).str.split(',', expand=True)
    df.columns = [f"col_{i}" for i in range(df.shape[1])]
    df = df.dropna(how="all")

# 🧼 Nettoyage intelligent des valeurs vides
for col in df.columns:
    unique_vals = df[col].dropna().unique()
    clean_vals = set([val.strip().lower() for val in unique_vals if val.strip() != ""])

    if all(val in ["yes", "no"] for val in clean_vals):
        df[col] = df[col].apply(lambda x: x.strip().lower() if x.strip().lower() in ["yes", "no"] else "no")
    elif df[col].str.replace('.', '', 1).str.isnumeric().all():
        df[col] = df[col].replace(r'^\s*$', '0', regex=True)
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    else:
        df[col] = df[col].replace(r'^\s*$', 'n/a', regex=True)

# 💾 Export
os.makedirs(output_dir, exist_ok=True)
df.to_csv(output_path, index=False, encoding='utf-8')
print(f"✅ Données nettoyées exportées avec succès : {output_path}")
