import os
import pandas as pd
import mysql.connector
from mysql.connector import Error

# 📁 Chemin vers les CSV nettoyés
CSV_DIR = r"H:\Git Hub\Analyse des Pals\2_cleaned\cleaned_palworld_data_Heidi"

# ⚙️ Paramètres de connexion à MySQL
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "palworld_database"
}

def clean_column_name(col):
    return col.strip().lower().replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_").replace("=", "_").replace("/", "_")

def main():
    for file in os.listdir(CSV_DIR):
        if file.endswith(".csv"):
            table_name = file.replace(".csv", "").strip().lower()
            file_path = os.path.join(CSV_DIR, file)

            print(f"🔄 Traitement : {file} → Table: {table_name}")

            try:
                df = pd.read_csv(file_path)
                df.columns = [clean_column_name(c) for c in df.columns]
                df = df.where(pd.notna(df), None)

                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor()

                placeholders = ", ".join(["%s"] * len(df.columns))
                columns = ", ".join(df.columns)

                create_stmt = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    {', '.join([f'{col} TEXT' for col in df.columns])}
                )
                """
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                cursor.execute(create_stmt)

                for row in df.itertuples(index=False, name=None):
                    insert_stmt = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                    try:
                        cursor.execute(insert_stmt, row)
                    except Error as e:
                        print(f"❌ Erreur d'insertion ligne: {e}")
                        continue

                conn.commit()
                cursor.close()
                conn.close()
                print(f"✅ Table '{table_name}' insérée avec succès ({len(df)} lignes)")

            except Exception as e:
                print(f"❌ Erreur globale pour {table_name}: {e}")

if __name__ == "__main__":
    main()
