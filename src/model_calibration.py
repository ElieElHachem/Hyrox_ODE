# src/model_calibration.py

import pandas as pd
from src.config import DEFAULT_MODEL_PARAMS

def calibrate_model(data):
    """
    Calibre les paramètres du modèle physiologique en se basant sur les données
    réelles du fichier CSV.
    """
    print("\n--- 2. Lancement de la Calibration Automatique ---")
    
    if data is None or data.empty:
        print("⚠️ Aucune donnée de calibration, utilisation des paramètres par défaut.")
        return DEFAULT_MODEL_PARAMS

    # On commence avec les paramètres par défaut comme base
    calibrated_params = DEFAULT_MODEL_PARAMS.copy()
    
    # Fréquence cardiaque de référence pour un effort "standard"
    baseline_hr = DEFAULT_MODEL_PARAMS['baseline_hr']

    print("Ajustement des coefficients de coût en fonction de vos données :")

    for param_key, default_value in DEFAULT_MODEL_PARAMS.items():
        if param_key.startswith('k_'):
            # Convertir la clé de paramètre en nom d'exercice (ex: k_sled_push -> Sled Push)
            exercise_name_parts = param_key.replace('k_', '').split('_')
            exercise_name = ' '.join([part.capitalize() for part in exercise_name_parts])
            
            if 'Run' in exercise_name:
                exercise_name = 'Course 1km'
            elif 'Ski Erg' in exercise_name:
                exercise_name = 'SkiErg'
            elif 'Row Erg' in exercise_name:
                exercise_name = 'RowErg'
            
            # Filtrer les données pour cet exercice à l'état "Frais"
            exercise_data = data[(data['Exercice'] == exercise_name)]
            
            if not exercise_data.empty and 'FC_Moyenne_BPM' in exercise_data.columns:
                # Calculer la FC moyenne pour cet exercice
                avg_hr = exercise_data['FC_Moyenne_BPM'].mean()
                
                if pd.notna(avg_hr) and avg_hr > 0:
                    # Calculer le facteur d'ajustement
                    adjustment_factor = avg_hr / baseline_hr
                    
                    # Mettre à jour le paramètre
                    new_value = default_value * adjustment_factor
                    calibrated_params[param_key] = new_value
                    
                    print(f"  - {exercise_name:<20}: FC moy.={avg_hr:.0f} bpm -> {param_key} ajusté à {new_value:.6f}")

    print("\n✅ Modèle calibré sur vos données.")
    return calibrated_params