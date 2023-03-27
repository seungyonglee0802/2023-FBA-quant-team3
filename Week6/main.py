import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
from datetime import datetime
from momentum import cross_sectional_momentum, time_series_momentum
from utils import json_to_df, performance_metrics, plot_cumulative_return_and_drawdown


def plot_cross_sectional_momentum(df, window_size=252, quantile=0.1):
    # Calculate Long-Only and Long-Short portfolios using cross-sectional momentum
    long_only, long_short = cross_sectional_momentum(df, window_size=window_size, quantile=quantile)

    # Calculate performance metrics for Long-Only portfolio
    CAGR, volatility, sharpe_ratio = performance_metrics(long_only)
    print(f"Cross-Sectional Long-Only:\nCAGR: {CAGR:.2f}, Volatility: {volatility:.2f}, Sharpe Ratio: {sharpe_ratio:.2f}")
    long_only_performance = {
        'cagr': CAGR,
        'volatility': volatility,
        'sharpe_ratio': sharpe_ratio
    }
    # Calculate performance metrics for Long-Short portfolio
    CAGR, volatility, sharpe_ratio = performance_metrics(long_short)
    print(f"Cross-Sectional Long-Short:\nCAGR: {CAGR:.2f}, Volatility: {volatility:.2f}, Sharpe Ratio: {sharpe_ratio:.2f}")
    long_short_performance = {
        'cagr': CAGR,
        'volatility': volatility,
        'sharpe_ratio': sharpe_ratio
    }

    kwargs = {
        'window_size': window_size,
        'quantile': quantile
    }
    # Plot cumulative return and drawdown for cross-sectional Long-Only portfolio
    plot_cumulative_return_and_drawdown(long_only, title='Cross-Sectional Long-Only', **long_only_performance, **kwargs)

    # Plot cumulative return and drawdown for cross-sectional Long-Short portfolio
    plot_cumulative_return_and_drawdown(long_short, title='Cross-Sectional Long-Short', **long_short_performance, **kwargs)


def plot_time_series_momentum(df, window_size=252):
    # Calculate Long-Only and Long-Short portfolios using time-series momentum
    long_only, long_short = time_series_momentum(df, window_size=window_size)

    # Calculate performance metrics for Long-Only time-series momentum portfolio
    CAGR, volatility, sharpe_ratio = performance_metrics(long_only)
    print(f"Time-Series Long-Only:\nCAGR: {CAGR:.2f}, Volatility: {volatility:.2f}, Sharpe Ratio: {sharpe_ratio:.2f}")
    long_only_performance = {
        'cagr': CAGR,
        'volatility': volatility,
        'sharpe_ratio': sharpe_ratio
    }

    # Calculate performance metrics for Long-Short time-series momentum portfolio
    CAGR, volatility, sharpe_ratio = performance_metrics(long_short)
    print(f"Time-Series Long-Short:\nCAGR: {CAGR:.2f}, Volatility: {volatility:.2f}, Sharpe Ratio: {sharpe_ratio:.2f}")
    long_short_performance = {
        'cagr': CAGR,
        'volatility': volatility,
        'sharpe_ratio': sharpe_ratio
    }

    kwargs = {
        'window_size': window_size,
    }
    # Plot cumulative return and drawdown for time-series Long-Only portfolio
    plot_cumulative_return_and_drawdown(long_only, title='Time-Series Long-Only', **long_only_performance, **kwargs)

    # Plot cumulative return and drawdown for time-series Long-Short portfolio
    plot_cumulative_return_and_drawdown(long_short, title='Time-Series Long-Short', **long_short_performance, **kwargs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, default='Week6/fai_close_data.json')
    parser.add_argument('--momentum_type', type=str, default='cross_sectional')
    parser.add_argument('--window_size', type=int, default=252)
    parser.add_argument('--quantile', type=float, default=0.1)
    args = parser.parse_args()

    df = json_to_df(args.input_file)

    if args.momentum_type == 'cross_sectional':
        plot_cross_sectional_momentum(df, window_size=args.window_size, quantile=args.quantile)
    elif args.momentum_type == 'time_series':
        plot_time_series_momentum(df, window_size=args.window_size)
    else:
        raise ValueError(f"Invalid momentum type: {args.momentum_type}")