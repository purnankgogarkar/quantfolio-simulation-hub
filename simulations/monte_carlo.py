import numpy as np
import pandas as pd

def run_monte_carlo(data, quantities, iterations):

    log_returns = np.log(data / data.shift(1)).dropna()

    mean_returns = log_returns.mean()
    cov_matrix = log_returns.cov()

    # Convert to numpy arrays
    mean_returns = mean_returns.values
    cov_matrix = cov_matrix.values

    # Add small noise to diagonal (regularization)
    cov_matrix += np.eye(len(cov_matrix)) * 1e-6

    simulated_returns = np.random.multivariate_normal(
        mean_returns,
        cov_matrix,
        iterations
    )

    simulated_prices = pd.DataFrame(
        simulated_returns,
        columns=data.columns
    )

    current_prices = data.iloc[-1]

    simulated_prices = (simulated_prices + 1) * current_prices.values

    portfolio_values = np.dot(simulated_prices, quantities[:len(data.columns)])

    current_value = np.dot(current_prices, quantities[:len(data.columns)])

    losses = current_value - portfolio_values

    return losses