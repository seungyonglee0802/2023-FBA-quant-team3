import numpy as np
import pandas as pd

def cross_sectional_momentum(df, window_size=252, quantile=0.1, rebalancing_period=21):
    returns = df.pct_change(fill_method=None).shift(-1)
    momentum = df.pct_change(periods=window_size, fill_method=None)

    long_only_returns = pd.DataFrame(np.nan, index=returns.index, columns=returns.columns)
    long_short_returns = pd.DataFrame(np.nan, index=returns.index, columns=returns.columns)

    counter = 0

    top_quantile = []
    top_half_quantile = []
    bottom_half_quantile = []

    for date, row in momentum[window_size:].iterrows():
        n = int(len(row) * quantile)

        if sum(~row.isna()) < n:
            raise ValueError(f"Number of stocks in the universe is less than {n}.")

        if counter % rebalancing_period == 0:
            top_quantile = row.dropna().nlargest(n).index
            top_half_quantile = row.dropna().nlargest(n // 2).index
            bottom_half_quantile = row.dropna().nsmallest(n // 2).index

        # TODO: Weighted return
        long_only_returns.loc[date, :] = np.where(long_only_returns.columns.isin(top_quantile), returns.loc[date, :], np.nan)
        long_short_returns.loc[date, :] = np.where(long_short_returns.columns.isin(top_half_quantile), returns.loc[date, :], np.nan)
        long_short_returns.loc[date, :] = np.where(long_short_returns.columns.isin(bottom_half_quantile), 1/(1+returns.loc[date, :])-1, long_short_returns.loc[date, :])

        counter += 1

    return long_only_returns, long_short_returns

def time_series_momentum(df, window_size=252, rebalancing_period=21):
    returns = df.pct_change(fill_method=None)
    rolling_mean = returns.rolling(window = window_size).mean()
    returns = returns.shift(-1)

    long_only_returns = pd.DataFrame(np.nan, index=returns.index, columns=returns.columns)
    long_short_returns = pd.DataFrame(np.nan, index=returns.index, columns=returns.columns)

    counter = 0

    # Initialize positive_mean_returns and negative_mean_returns
    first_row = rolling_mean.iloc[0]
    positive_mean_returns = first_row > 0
    negative_mean_returns = first_row < 0

    for date, row in rolling_mean.iterrows():
        if counter % rebalancing_period == 0:
            positive_mean_returns = row > 0
            negative_mean_returns = row < 0

        long_only_returns.loc[date, :] = np.where(positive_mean_returns, returns.loc[date, :], np.nan)
        long_short_returns.loc[date, :] = np.where(positive_mean_returns, returns.loc[date, :], np.nan)
        long_short_returns.loc[date, :] = np.where(negative_mean_returns, 1/(1+returns.loc[date, :])-1, long_short_returns.loc[date, :])

        counter += 1

    return long_only_returns, long_short_returns
