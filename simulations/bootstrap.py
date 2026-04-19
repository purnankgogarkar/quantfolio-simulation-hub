import numpy as np

def run_bootstrap_simulation(data, quantities, iterations):

    returns = data.pct_change().dropna()

    # FIX: Ensure quantities array matches number of stocks
    quantities = np.array(quantities).flatten()
    
    if len(quantities) != len(returns.columns):
        raise ValueError(f"Quantities mismatch: {len(quantities)} vs {len(returns.columns)} stocks")

    # Normalize quantities to sum to 1
    quantities_normalized = quantities / np.sum(quantities)

    simulated_indices = np.random.choice(len(returns), size=iterations, replace=True)
    
    simulated = returns.iloc[simulated_indices].reset_index(drop=True)

    portfolio_returns = simulated.dot(quantities_normalized)

    losses = -portfolio_returns.values

    return losses