import numpy as np
import pandas as pd
from data_loader import load_kospi


def backtest_daily(close_df, signal_dict):
    """
    Backtest a strategy using daily signals.
    """
    num_universe = len(close_df.columns)
    returns = close_df.pct_change(fill_method=None).shift(-1)
    strategy_returns = pd.Series(dtype="float64")
    signal = None
    strategy_start_date = list(signal_dict.keys())[0]
    for date, row in returns.iterrows():
        if date in signal_dict.keys():
            signal = signal_dict[date]
            assert len(signal) == num_universe
            # normalize signal by absolute value
            signal = signal / np.abs(signal).sum()
        if signal is None:
            continue
        # if signal is long only
        if (signal >= 0).all():
            strategy_returns.loc[date] = (signal * returns.loc[date, :]).sum()
        # if signal is long short
        else:
            negative_mask = signal < 0
            positive_signal = signal.copy()
            positive_signal[negative_mask] = 0

            negative_signal = abs(signal.copy())
            negative_signal[~negative_mask] = 0

            strategy_returns.loc[date] = (
                positive_signal * returns.loc[date, :]
            ).sum() + (negative_signal * (1 / (1 + returns.loc[date, :]) - 1)).sum()

    strategy_returns.index = pd.to_datetime(strategy_returns.index)
    benchmark_returns = get_benchmark_returns(start_date=strategy_start_date)
    return strategy_returns, benchmark_returns


def get_benchmark_returns(start_date=None):
    """
    Backtest a buy-and-hold strategy for KOSPI.
    """
    close_df = load_kospi(start_date)
    benchmark_returns = close_df.pct_change(fill_method=None).shift(-1)
    return benchmark_returns
