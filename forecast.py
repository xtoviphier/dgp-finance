import numpy as np
from scipy import stats

def ols_forecast(values, next_index=None):
    """
    Simple OLS forecast: y = mx + b
    values: array of historical values (e.g., cash flow)
    returns: (next_period_label, forecast_value, confidence_interval_width)
    """
    n = len(values)
    x = np.arange(1, n+1)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, values)
    
    # Forecast next period
    next_x = n + 1 if next_index is None else next_index
    forecast = slope * next_x + intercept
    
    # 95% confidence interval (simplified)
    ci_width = 1.96 * std_err * np.sqrt(1 + 1/n + (next_x - np.mean(x))**2 / np.sum((x - np.mean(x))**2))
    
    return f"Period {next_x}", forecast, ci_width