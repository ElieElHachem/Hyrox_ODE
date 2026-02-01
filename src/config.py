# src/config.py

# --- Fichiers ---
CALIBRATION_DATA_FILE = 'data/hyrox_calibration_data.csv'

# --- Paramètres de Simulation ---
NUM_STRATEGIES_TO_SIMULATE = 2000
ENERGY_INITIAL = 1
ENERGY_CRITICAL_THRESHOLD = 0.02

# --- Séquence Hyrox ---
VARIABLE_NAMES = [
    'time_run1', 'time_rox_1', 'time_ski_erg', 'time_rox_2',
    'time_run2', 'time_rox_3', 'time_sled_push', 'time_rox_4',
    'time_run3', 'time_rox_5', 'time_sled_pull', 'time_rox_6',
    'time_run4', 'time_rox_7', 'time_burpees', 'time_rox_8',
    'time_run5', 'time_rox_9', 'time_row_erg', 'time_rox_10',
    'time_run6', 'time_rox_11', 'time_farmers_carry', 'time_rox_12',
    'time_run7', 'time_rox_13', 'time_sandbag_lunges', 'time_rox_14',
    'time_run8', 'time_rox_15', 'time_wall_balls'
]

# --- Bornes de Performance [rapide, lent] ---
PERFORMANCE_BOUNDS = {
    'time_run': [210, 480],          # 3:30 à 8:00 /km
    'time_rox': [20, 60],           # Transitions (besoin de récup)
    'time_ski_erg': [180, 360],      # 3:00 à 6:00
    'time_sled_push': [200, 300],        
    'time_sled_pull': [150, 330],    # 2:30 à 5:30
    'time_burpees': [140, 420],      # 2:20 à 7:00
    'time_row_erg': [195, 280],      # 3:15 à 5:30
    'time_farmers_carry': [70, 210],     # 1:10 à 3:30
    'time_sandbag_lunges': [180, 480],
    'time_wall_balls': [200, 510]        
}

# RETOUR AUX VALEURS STANDARDS (Calibration affinera)
DEFAULT_MODEL_PARAMS = {
    'k_run': 0.000035, 'alpha_run': 2.2,
    'k_rox': 0.00015,  
    'k_ski_erg': 0.00019, 'k_sled_push': 0.00045, 'k_sled_pull': 0.00045,
    'k_burpees': 0.00035, 'k_row_erg': 0.00019, 'k_farmers_carry': 0.00021,
    'k_sandbag_lunges': 0.00035, 'k_wall_balls': 0.00045,
    'recovery_rate': 0.0001
}