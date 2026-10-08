import numpy as np

def calculate_portfolio_var(
    weights: np.ndarray, 
    returns_cov_matrix: np.ndarray, 
    portfolio_value: float, 
    time_horizon_days: int = 10, 
    confidence_level: float = 0.99,
    simulations: int = 1_000_000
) -> float:
    """
    Computes Value at Risk (VaR) using Monte Carlo Simulation.
    Determines maximum expected loss under extreme market conditions.
    """
    mean_returns = np.zeros(len(weights))
    cholesky_decomp = np.linalg.cholesky(returns_cov_matrix)
    
    # Generate random market shocks
    uncorrelated_sims = np.random.normal(size=(simulations, len(weights)))
    correlated_sims = uncorrelated_sims @ cholesky_decomp.T
    
    # Calculate simulated portfolio returns
    portfolio_sim_returns = correlated_sims @ weights
    scaled_returns = portfolio_sim_returns * np.sqrt(time_horizon_days)
    
    # Extract VaR threshold at 99% confidence
    var_percentile = np.percentile(1 - confidence_level, scaled_returns)
    max_loss = portfolio_value * std_loss_percentile = np.abs(np.percentile(scaled_returns, (1 - confidence_level) * 100))
    
    return portfolio_value * std_loss_percentile

# Portfolio setup ($1 Billion Assets under Management)
weights = np.array([0.4, 0.35, 0.25])
cov_matrix = np.array([
    [0.0004, 0.0002, 0.0001],
    [0.0002, 0.0003, 0.00015],
    [0.0001, 0.00015, 0.0005]
])

var_99 = calculate_portfolio_var(weights, cov_matrix, portfolio_value=1_000_000_000)
print(f"10-Day 99% Value at Risk: ${var_99:,.2f}")