import numpy as np

def run_stress_test(data, quantities):

    current_prices = data.iloc[-1]

    # FIX: Ensure quantities array matches number of stocks
    quantities = np.array(quantities).flatten()
    
    if len(quantities) != len(current_prices):
        raise ValueError(f"Quantities mismatch: {len(quantities)} vs {len(current_prices)} stocks")

    stress_drop = 0.1

    stressed_prices = current_prices * (1 - stress_drop)

    portfolio_value = np.dot(current_prices.values, quantities)

    stressed_value = np.dot(stressed_prices.values, quantities)

    loss = portfolio_value - stressed_value

    return np.array([loss])