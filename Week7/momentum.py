import numpy as np


def cross_sectional_momentum(df, window_size=252, quantile=0.1, rebalancing_period=21):
    momentum = df.pct_change(periods=window_size, fill_method=None)
    long_only_signal = {}
    long_short_signal = {}

    counter = 0

    for date, row in momentum[window_size:].iterrows():
        n = int(len(row) * quantile)
        if sum(~row.isna()) < n:
            raise ValueError(f"Number of stocks in the universe is less than {n}.")

        if counter % rebalancing_period == 0:
            top_quantile = row.dropna().nlargest(n).index
            top_half_quantile = row.dropna().nlargest(n // 2).index
            bottom_half_quantile = row.dropna().nsmallest(n // 2).index
            long_only_signal[date] = np.array(
                [1 if i in top_quantile else 0 for i in row.index]
            )
            long_short_signal[date] = np.array(
                [
                    1
                    if i in top_half_quantile
                    else -1
                    if i in bottom_half_quantile
                    else 0
                    for i in row.index
                ]
            )

        counter += 1

    return long_only_signal, long_short_signal


def time_series_momentum(df, window_size=252, rebalancing_period=21):
    rolling_mean = df.pct_change(fill_method=None).rolling(window=window_size).mean()
    long_only_signal = {}
    long_short_signal = {}

    counter = 0

    for date, row in rolling_mean[window_size:].iterrows():
        if counter % rebalancing_period == 0:
            long_only_signal[date] = np.array([1 if i > 0 else 0 for i in row])
            long_short_signal[date] = np.array(
                [1 if i > 0 else -1 if i < 0 else 0 for i in row]
            )

        counter += 1

    return long_only_signal, long_short_signal
