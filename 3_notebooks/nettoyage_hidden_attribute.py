import pandas as pd
import os

# 📂 Détection dynamique des chemins
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "..", "1_data")
output_dir = os.path.join(script_dir, "..", "2_cleaned", "cleaned_palworld_data_Heidi")

input_file = "Palworld_Data-hide pallu attributes.csv"
output_file = "hidden_attribute_clean_filtered.csv"

# 📥 Chargement brut du fichier CSV
df = pd.read_csv(os.path.join(data_dir, input_file), dtype=str, keep_default_na=False)

# 🔤 Normalisation des noms de colonnes
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# ✅ Colonnes à conserver (selon ta spécification)
columns_needed = [
    "name", "code_name", "overridenametextid", "nameprefixid", "overridepartnerskilltextid",
    "tribe", "bpclass", "pictorial_id", "zukanindexsuffix", "size", "rarity",
    "element_1", "element_2", "genuscategory", "hp", "melee_attack", "remote_attack",
    "defense", "support", "craftspeed", "being_damage_multiplier", "capture_probability",
    "experience_multiplier", "price", "airresponse", "aisightresponse", "slow_walking_speed",
    "walking_speed", "running_speed", "riding_sprint_speed", "handling_speed", "isboss",
    "istowerboss", "battlebgm", "ignoreleanback", "ignoreblowaway", "maxfullstomach",
    "fullstomachdecreaserate", "foodamount", "viewingdistance", "viewingangle", "hearingrate",
    "noosetrap", "nocturnal", "biologicalgrade", "predator", "edible", "endurance",
    "male_probability", "fecundity", "breathing_fire", "watering", "planting",
    "generate_electricity", "manual", "collection", "logging", "mining", "oilextraction",
    "pharmaceutical", "cool_down", "carry", "pasture",
    "passive_skill_1", "passive_skill_2", "passive_skill_3", "passive_skill_4"
]

# 🔍 Garde seulement les colonnes disponibles
available_columns = [col for col in columns_needed if col in df.columns]
df = df[available_columns]

# 🔄 Nettoyage ligne par ligne
for col in df.columns:
    vals = df[col].dropna().unique()
    clean_vals = set([v.strip().lower() for v in vals if v.strip() != ""])
    
    if all(v in ["yes", "no"] for v in clean_vals):
        df[col] = df[col].apply(lambda x: x.strip().lower() if x.strip().lower() in ["yes", "no"] else "no")
    elif df[col].str.replace('.', '', 1).str.isnumeric().all():
        df[col] = df[col].replace(r'^\s*$', '0', regex=True)
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    else:
        df[col] = df[col].replace(r'^\s*$', 'n/a', regex=True)

# 🧽 Suppression des doublons
df = df.drop_duplicates()

# 💾 Sauvegarde du fichier nettoyé
os.makedirs(output_dir, exist_ok=True)
export_path = os.path.join(output_dir, output_file)
df.to_csv(export_path, index=False, encoding='utf-8')

print(f"✅ Données nettoyées exportées ici : {export_path}")
