# src/data_loader.py

import pandas as pd
import os


def load_and_validate_data(filepath):
    """Charge et valide les données de calibration."""
    print(f"--- 1. Chargement des données depuis '{filepath}' ---")
    if not os.path.exists(filepath):
        print(f"❌ ERREUR: Fichier '{filepath}' non trouvé.")
        return None
        
    df = pd.read_csv(filepath)
    required_cols = ['Exercice', 'Temps_Secondes', 'Etat_Initial']
    if not all(col in df.columns for col in required_cols):
        print(f"❌ ERREUR: Le fichier doit contenir : {required_cols}")
        return None
        
    print("✅ Données chargées avec succès.")
    return df
