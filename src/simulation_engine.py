# src/simulation_engine.py

import numpy as np
from scipy.integrate import solve_ivp
from src.config import ENERGY_INITIAL, ENERGY_CRITICAL_THRESHOLD

def run_hyrox_ode_simulation(strategy_vector, model_params, activities_config, return_details=False):
    """
    Simule une course complète.
    Si return_details est True, retourne l'historique complet de la simulation.
    """

    def energy_model(t, E, activity_params):
        """L'équation différentielle de l'énergie."""
        if E[0] <= 0:
            return 0
            
        cost_key = activity_params['cost_key']
        intensity = activity_params['intensity']
        model_params = activity_params['model_params']
        
        if 'run' in cost_key:
            cost = model_params['k_run'] * (intensity ** model_params['alpha_run'])
        else:
            power = 100 / intensity
            cost = model_params[cost_key] * power
        
        fatigue_factor = 1 + (1 - E[0])**2
        dE_dt = model_params['recovery_rate'] - (cost * fatigue_factor)
        return dE_dt

    total_time = 0
    current_energy = ENERGY_INITIAL
    simulation_log = []

    for i, activity in enumerate(activities_config):
        segment_time = strategy_vector[i]
        
        intensity = (activity['distance'] / segment_time) if activity['type'] == 'run' else segment_time
        activity_params = {'cost_key': activity['cost_key'], 'intensity': intensity, 'model_params': model_params}

        sol = solve_ivp(
            energy_model, [0, segment_time], [current_energy],
            args=(activity_params,), dense_output=True, method='RK45', max_step=10
        )

        min_energy_in_segment = np.min(sol.y)
        if min_energy_in_segment < ENERGY_CRITICAL_THRESHOLD:
            return np.inf, None

        current_energy = sol.y[0, -1]
        
        if return_details:
            simulation_log.append({
                'segment_name': activity['cost_key'].replace('k_', 'time_'),
                'time_points': sol.t + total_time,
                'energy_points': sol.y[0]
            })
        
        total_time += segment_time
        
    return total_time, simulation_log