import pandas as pd
import os

# 📂 Chemins
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "..", "1_data")
output_dir = os.path.join(script_dir, "..", "2_cleaned", "cleaned_palworld_data_Heidi")

input_file = "Palworld_Data-comparison of ordinary BOSS attributes.csv"
output_file = "ordinary_boss_clean_fixed.csv"
input_path = os.path.join(data_dir, input_file)
output_path = os.path.join(output_dir, output_file)

# 📥 Chargement
df = pd.read_csv(input_path, dtype=str, keep_default_na=False)

# 🧹 Nettoyage de base
df.dropna(axis=1, how='all', inplace=True)
df = df.loc[:, ~df.columns.str.contains('^Unnamed', case=False, na=False)]
df.drop_duplicates(inplace=True)
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# 🏷️ Renommage manuel si besoin
if "riding_speed_(boss_is_100_higher)" in df.columns:
    df.rename(columns={"riding_speed_(boss_is_100_higher)": "riding_speed"}, inplace=True)

# ⚠️ Cas d'encodage mauvais (1 seule colonne)
if df.shape[1] == 1:
    print("⚠️ Une seule colonne détectée — tentative de découpage automatique...")
    col = df.columns[0]
    df = df[col].astype(str).str.split(',', expand=True)
    df.columns = [f"col_{i}" for i in range(df.shape[1])]
    df.dropna(how="all", inplace=True)

# 🧮 Colonnes numériques forcées
forced_numeric_cols = ["hp", "remote_attack", "riding_speed"]

# 🧼 Nettoyage
for col in df.columns:
    if col == "name":
        df[col] = df[col].replace(r'^\s*$', 'n/a', regex=True)
    elif col in forced_numeric_cols:
        df[col] = df[col].replace(r'^\s*$', '0', regex=True)
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    else:
        vals = df[col].dropna().unique()
        cleaned_vals = set([v.strip().lower() for v in vals if v.strip() != ""])
        if all(v in ["yes", "no"] for v in cleaned_vals):
            df[col] = df[col].apply(lambda x: x.strip().lower() if x.strip().lower() in ["yes", "no"] else "no")
        elif df[col].str.replace('.', '', 1).str.isnumeric().all():
            df[col] = df[col].replace(r'^\s*$', '0', regex=True)
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        else:
            df[col] = df[col].replace(r'^\s*$', 'n/a', regex=True)

# 💾 Export
os.makedirs(output_dir, exist_ok=True)
df.to_csv(output_path, index=False, encoding='utf-8')
print(f"✅ Données nettoyées et exportées avec succès : {output_path}")
