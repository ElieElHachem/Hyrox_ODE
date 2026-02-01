
# Hyrox Strategy Optimization Model

## 1. Introduction

This project presents an advanced mathematical model for determining the optimal race strategy for a Hyrox-type competition. Using an approach based on ordinary differential equations (ODE), the system models an athlete's energy expenditure throughout the event to predict a final time and associated pacing strategy.

The objective is to provide the athlete with a personalized race plan that minimizes total time while managing energy expenditure to avoid premature exhaustion.

---

## 2. Methodology

The model treats the athlete as a dynamic system whose main state is the energy level `E(t)`. The evolution of this energy is governed by a differential equation that accounts for the energy costs of each segment of the event (running and exercise stations, including Rox Zones).

The process unfolds in three distinct phases:

1.  **Data Collection**: The athlete records performance data (times, heart rate) on specific exercises.
2.  **Model Calibration**: The system uses this data to personalize the parameters of a physiological model. Energy cost coefficients (`k_...`) are adjusted to reflect the athlete's specific capabilities.
3.  **Optimization via Simulation**: The calibrated model simulates a large number of race strategies (`1000` by default). Strategies leading to exhaustion are eliminated, and the fastest among viable strategies is identified as optimal.

---

## 3. Project Architecture

The project is structured in a modular way to ensure code clarity and maintainability.

```
HyroxODE/
│
├── data/
│   └── hyrox_calibration_data.csv       # Training data file
│
├── src/
│   ├── __init__.py                      # Package initialization file
│   ├── config.py                        # Global and configurable parameters
│   ├── data_loader.py                   # Data loading module
│   ├── model_calibration.py             # Model calibration module
│   ├── simulation_engine.py             # Simulation core (ODE solver)
│   └── optimizer.py                     # Strategy optimization module
│
├── main.py                              # Main application entry point
└── requirements.txt                     # Project dependencies
```

### Module Descriptions

* **`main.py`**: Orchestrates the entire process: data loading, calibration, optimization, and result display.
* **`data/hyrox_calibration_data.csv`**: CSV file containing training logs. Must include at minimum the columns `Exercise`, `Time_Seconds`, `Initial_State`, and `Average_HR_BPM` for calibration.
* **`src/config.py`**: Centralizes all user-modifiable parameters, such as data file path, number of simulations, performance bounds (`PERFORMANCE_BOUNDS`), and default physiological parameters.
* **`src/data_loader.py`**: Contains the `load_and_validate_data` function, responsible for reading and structurally validating the CSV file.
* **`src/model_calibration.py`**: Implements the `calibrate_model` function. It adjusts energy cost coefficients (`k_...`, `k_rox`) based on the athlete's average heart rate for each exercise compared to a reference value.
* **`src/simulation_engine.py`**: Contains the model core, `run_hyrox_ode_simulation`. This function simulates a complete race for a given strategy by solving the energy differential equation segment by segment (including Rox Zones).
* **`src/optimizer.py`**: Manages the optimization phase. It generates a design of experiments via Latin hypercube sampling (LHS), runs simulations for each strategy, and identifies the best performance among viable results.

---

## 4. Rox Zone Component

The Rox Zone is a specialized obstacle segment introduced in modern Hyrox formats. It is treated by the optimization model as a distinct segment type, similar to exercise stations but with its own energy cost parameters.

### Key Features:
* **Dedicated Energy Cost Parameter**: Uses `k_rox` coefficient, calibrated separately from traditional stations.
* **Time-Performance Trade-off**: Like exercise stations, energy cost follows the relationship $k_{rox} \cdot \frac{100}{T_{rox}}$, allowing the optimizer to balance speed vs. energy conservation.
* **Integration in Strategy Space**: Rox Zones are included in the optimization strategy vector, enabling the model to determine optimal time allocation.

---

## 5. Usage Guide

### Prerequisites

* Python 3.11 at MAXIMUM
* Libraries listed in `requirements.txt`

### Execution Steps

1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Populate calibration data**:
    * Open the file `data/hyrox_calibration_data.csv`.
    * Fill it with your own training data while respecting the column format. Make sure to include sessions in both `Fresh` and `Fatigued` states for accurate calibration of fatigue impact (allows determining the difference between states).

3.  **Configure parameters (optional)**:
    * Open the file `src/config.py`.
    * Adjust `PERFORMANCE_BOUNDS` to match your realistic performance range (your fastest and slowest possible times for each segment).
    * You can also adjust `NUM_STRATEGIES_TO_SIMULATE` to increase the number of simulations (more precise, but slower).

4.  **Run the program**:
    * From the root of the `Hyrox_ODE` folder, execute the following command in your terminal:
    ```bash
    python main.py
    ```

### Interpreting Results

The script will display in the console:
1.  The status of data loading and calibration, including calculated coefficient adjustments.
2.  A series of diagnostic messages (`⚠️ Failed on segment...`) indicating strategies that were eliminated. This is normal behavior.
3.  A final table presenting the **optimal race strategy found** and the **estimated total time**.
4.  A visualization graph (`hyrox_optimal_strategy.png`) showing pacing strategy and energy evolution throughout the race.

---

## 6. Limitations and Future Improvements

* **Simplified Energy Model**: The model uses a single energy reservoir without distinguishing localized muscle fatigue from central fatigue.
* **Basic Calibration**: The `calibrate_model` function uses a simple ratio-based method using heart rate. More advanced statistical regression could provide more accurate coefficients.
* **Sampling-Based Optimization**: The script uses LHS, which is a sampling method rather than an intelligent optimization algorithm. For deeper optimization search, algorithms like Bayesian Optimization could be implemented.
* **Rox Zone Modeling**: Current implementation treats Rox Zones with constant difficulty. Future versions could incorporate variable difficulty levels or athlete-specific Rox Zone performance profiles.

---

## 7. Installation and Quick Start

```bash
# Clone or download the project
cd Hyrox_ODE

# Install dependencies
pip install -r requirements.txt

# Run the optimizer
python main.py
```

The results will be displayed in the console and a strategy graph will be saved as `hyrox_optimal_strategy.png`.

