import numpy as np

def run_historical_simulation(data, quantities):

    returns = data.pct_change().dropna()

    # FIX: Ensure quantities array matches number of stocks
    quantities = np.array(quantities).flatten()
    
    if len(quantities) != len(returns.columns):
        raise ValueError(f"Quantities mismatch: {len(quantities)} vs {len(returns.columns)} stocks")

    # Normalize quantities to sum to 1
    quantities_normalized = quantities / np.sum(quantities)

    portfolio_returns = returns.dot(quantities_normalized)

    losses = -portfolio_returns.values

    return losses