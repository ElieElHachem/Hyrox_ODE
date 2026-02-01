# main.py

import matplotlib.pyplot as plt
import numpy as np
from src.config import CALIBRATION_DATA_FILE, VARIABLE_NAMES, ENERGY_CRITICAL_THRESHOLD
from src.data_loader import load_and_validate_data
from src.model_calibration import calibrate_model
from src.optimizer import find_optimal_strategy

def plot_results(best_strategy, simulation_log, output_filename="hyrox_optimal_strategy.png"):
    """Crée et sauvegarde un graphique de la stratégie et de l'énergie."""
    if not simulation_log:
        return
        
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(18, 12)) # Plus large pour accommoder les segments Rox
    
    # --- Graphique 1: Pacing (Temps par segment) ---
    segment_times = best_strategy[VARIABLE_NAMES].values
    
    # Code couleur : Run=Skyblue, Rox=LightGray, Station=SteelBlue
    colors = []
    for name in VARIABLE_NAMES:
        if 'run' in name and 'rox' not in name:
            colors.append('skyblue')
        elif 'rox' in name:
            colors.append('lightgray')
        else:
            colors.append('steelblue')

    # Étiquettes simplifiées pour l'axe X
    segment_labels = [name.replace('time_', '').replace('_', ' ').title() for name in VARIABLE_NAMES]
    
    ax1.bar(segment_labels, segment_times, color=colors, edgecolor='grey')
    ax1.set_ylabel('Temps par Segment (secondes)')
    ax1.set_title('Stratégie de Course Optimale (Avec Roxzone)')
    ax1.tick_params(axis='x', rotation=90, labelsize='small')
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # --- Graphique 2: Évolution de l'Énergie ---
    full_time = []
    full_energy = []
    segment_end_times = []
    
    for log in simulation_log:
        full_time.extend(log['time_points'])
        full_energy.extend(log['energy_points'])
        if log['time_points'].any():
            segment_end_times.append(log['time_points'][-1])

    full_time = np.array(full_time)
    full_energy = np.array(full_energy)
    
    ax2.plot(full_time / 60, full_energy * 100, label='Niveau d\'énergie', color='green', linewidth=2)
    ax2.axhline(y=ENERGY_CRITICAL_THRESHOLD * 100, color='r', linestyle='--', label=f'Seuil Critique ({ENERGY_CRITICAL_THRESHOLD*100:.0f}%)')
    
    # Lignes verticales segments
    for end_time in segment_end_times:
        ax2.axvline(x=end_time / 60, color='gray', linestyle=':', linewidth=0.5, alpha=0.5)
        
    ax2.set_xlabel('Temps de Course (minutes)')
    ax2.set_ylabel('Énergie Restante (%)')
    ax2.set_title('Évolution de l\'Énergie (Gestion physiologique)')
    ax2.set_ylim(0, 105)
    ax2.set_xlim(0, full_time.max() / 60)
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig(output_filename)
    print(f"\n✅ Graphique de la stratégie sauvegardé sous : {output_filename}")


def display_results(best_strategy):
    """Affiche la meilleure stratégie de manière lisible."""
    if best_strategy is None:
        return
        
    print("\n" + "="*50)
    print("🏆 STRATÉGIE DE COURSE OPTIMALE (AVEC ROX) 🏆")
    print("="*50)
    
    total_minutes = best_strategy['total_time_seconds'] / 60
    print(f"\nTemps total estimé : {total_minutes:.2f} minutes ({int(total_minutes)}m {int((total_minutes % 1) * 60)}s)")
    
    print("\n--- Détails du Pacing ---")
    
    # Affichage groupé pour lisibilité
    for i, name in enumerate(VARIABLE_NAMES):
        value = best_strategy[name]
        minutes, seconds = divmod(value, 60)
        
        label = name.replace('time_', '').replace('_', ' ').title()
        time_str = f"{int(minutes):02d}:{int(seconds):02d}"
        
        # Ajout d'un saut de ligne visuel après chaque bloc (Run + Rox + Station + Rox) ?
        # Ou simplement marquer les Rox différemment
        prefix = "  ↳ Rox" if 'rox' in name else "- " + label
        if 'rox' in name:
            print(f"{'':<4}Rox       : {time_str} ({int(value)}s)")
        elif 'run' in name:
            print(f"- {label:<22}: {time_str} /km")
        else:
            print(f"- {label:<22}: {time_str}")
            
    print("\n" + "="*50)

if __name__ == "__main__":
    # Phase 1: Données
    calibration_data = load_and_validate_data(CALIBRATION_DATA_FILE)
    
    # Phase 1.5: Calibration
    personal_model_params = calibrate_model(calibration_data)
    
    # Phase 2: Optimisation
    optimal_strategy, simulation_log = find_optimal_strategy(personal_model_params)
    
    # Affichage
    display_results(optimal_strategy)
    plot_results(optimal_strategy, simulation_log)