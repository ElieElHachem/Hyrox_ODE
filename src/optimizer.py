# src/optimizer.py

import numpy as np
import pandas as pd
import pyDOE2 as doe
from src.config import VARIABLE_NAMES, PERFORMANCE_BOUNDS, NUM_STRATEGIES_TO_SIMULATE
from src.simulation_engine import run_hyrox_ode_simulation

def find_optimal_strategy(model_params):
    """Orchestre la génération, la simulation et l'analyse des stratégies."""
    print("\n--- 3. Lancement de l'Optimisation (avec Roxzone) ---")
    
    # Configuration dynamique des activités
    activities_config = []
    for name in VARIABLE_NAMES:
        if 'run' in name and 'rox' not in name:
            activity_type = 'run'
            cost_key_name = 'k_run'
            distance = 1000
        elif 'rox' in name:
            activity_type = 'station' # Traité comme temps pur (intensité variable)
            cost_key_name = 'k_rox'
            distance = None
        else:
            activity_type = 'station'
            # Mappe "time_sled_push" -> "k_sled_push"
            cost_key_name = name.replace('time_', 'k_')
            distance = None
            
        activities_config.append({
            'type': activity_type,
            'distance': distance,
            'cost_key': cost_key_name
        })

    # Construction de la matrice des bornes
    bounds_list = []
    for name in VARIABLE_NAMES:
        if 'run' in name and 'rox' not in name:
            bounds_list.append(PERFORMANCE_BOUNDS['time_run'])
        elif 'rox' in name:
            bounds_list.append(PERFORMANCE_BOUNDS['time_rox'])
        else:
            bounds_list.append(PERFORMANCE_BOUNDS[name])
            
    bounds_matrix = np.array(bounds_list)
    
    # Génération du plan d'expérience (Latin Hypercube Sampling)
    lhd_norm = doe.lhs(len(VARIABLE_NAMES), samples=NUM_STRATEGIES_TO_SIMULATE, criterion='maximin')
    doe_plan = bounds_matrix[:, 0] + lhd_norm * (bounds_matrix[:, 1] - bounds_matrix[:, 0])

    print(f"🔬 Simulation de {NUM_STRATEGIES_TO_SIMULATE} stratégies sur {len(VARIABLE_NAMES)} segments...")
    
    # Simulation
    results_times = [run_hyrox_ode_simulation(strategy, model_params, activities_config)[0] for strategy in doe_plan]

    print("📊 Analyse des résultats...")
    results_df = pd.DataFrame(doe_plan, columns=VARIABLE_NAMES)
    results_df['total_time_seconds'] = results_times
    
    successful = results_df[results_df['total_time_seconds'] != np.inf]
    if successful.empty:
        print("❌ Aucune stratégie viable trouvée. Essayez d'élargir vos bornes ou d'augmenter le seuil d'énergie.")
        return None, None

    best_strategy_row = successful.loc[successful['total_time_seconds'].idxmin()]
    
    print("📈 Re-simulation de la meilleure stratégie pour générer le graphique...")
    best_strategy_vector = best_strategy_row[VARIABLE_NAMES].values
    _, simulation_log = run_hyrox_ode_simulation(best_strategy_vector, model_params, activities_config, return_details=True)

    return best_strategy_row, simulation_log