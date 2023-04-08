import numpy as np
import pandas as pd


def backtest_daily(close_df, signal_dict):
    """
    Backtest a strategy using daily signals.
    """
    returns = close_df.pct_change(fill_method=None).shift(-1)
    strategy_returns = pd.Series(np.nan, index=returns.index)
    signal = None
    for date, row in returns.iterrows():
        if date in signal_dict.keys():
            signal = signal_dict[date]
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

    return strategy_returns
