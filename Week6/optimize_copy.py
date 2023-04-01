import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from momentum import cross_sectional_momentum, time_series_momentum
from utils import json_to_df, performance_metrics

def find_best_parameters(df, momentum_type, trade_type, window_sizes, rebalancing_periods):
    best_sharpe_ratio = -np.inf
    best_window_size = None
    best_quantile = None
    sharpe_ratios = {}

    for window_size, rebalancing_period in itertools.product(window_sizes, rebalancing_periods):
        if momentum_type == 'cross_sectional':
            long_only, long_short = cross_sectional_momentum(df, window_size=window_size, rebalancing_period=rebalancing_period)
        elif momentum_type == 'time_series':
            long_only, long_short = time_series_momentum(df, window_size=window_size, rebalancing_period=rebalancing_period)
        else:
            raise ValueError(f"Invalid momentum type: {momentum_type}")
        
        if trade_type == 'long_only':
            _, _, sharpe_ratio = performance_metrics(long_only)
        elif trade_type == 'long_short':
            _, _, sharpe_ratio = performance_metrics(long_short)

        sharpe_ratios[(window_size, rebalancing_period)] = sharpe_ratio

        if sharpe_ratio > best_sharpe_ratio:
            best_sharpe_ratio = sharpe_ratio
            best_window_size = window_size
            best_rebalancing_period = rebalancing_period

    print(f"Best Sharpe ratio: {best_sharpe_ratio:.2f} (window size = {best_window_size}, rebalacing period = {best_rebalancing_period})")

    return sharpe_ratios

df = json_to_df('Week6/fai_close_data.json')
window_sizes=[63, 126, 189, 252, 315, 378, 441, 504]
rebalancing_periods=[5, 10, 21, 42, 63]

sharpe_ratios = find_best_parameters(df, trade_type='long_only', momentum_type='cross_sectional', window_sizes=window_sizes, rebalancing_periods=rebalancing_periods)

# Plot the results as a heatmap
sharpe_ratio_grid = np.zeros((len(window_sizes), len(rebalancing_periods)))
for i, window_size in enumerate(window_sizes):
    for j, rebalancing_period in enumerate(rebalancing_periods):
        sharpe_ratio_grid[i, j] = sharpe_ratios[(window_size, rebalancing_period)]

plt.figure(figsize=(8, 6))
sns.heatmap(sharpe_ratio_grid, cmap='RdYlGn', annot=True, fmt='.2f', xticklabels=rebalancing_periods, yticklabels=window_sizes)
plt.xlabel('Rebalancing Period')
plt.ylabel('Window Size')
plt.title('Sharpe Ratio Grid')
plt.show()
