import numpy as np
import pandas as pd

def cross_sectional_momentum(df, window_size=252, quantile=0.1, rebalancing_period=30):
    returns = df.pct_change().shift(-1)
    momentum = df.pct_change(periods=window_size)

    long_only_returns = pd.DataFrame(np.nan, index=returns.index, columns=returns.columns)
    long_short_returns = pd.DataFrame(np.nan, index=returns.index, columns=returns.columns)

    counter = 0

    top_quantile = []
    top_half_quantile = []
    bottom_half_quantile = []

    for date, row in momentum.iterrows():
        n = int(len(row) * quantile)

        if sum(~row.isna()) < n:
            continue

        if counter % rebalancing_period == 0:
            top_quantile = row.nlargest(n).index
            top_half_quantile = row.nlargest(n // 2).index
            bottom_half_quantile = row.nsmallest(n // 2).index

        # TODO: Weighted return
        long_only_returns.loc[date, :] = np.where(long_only_returns.columns.isin(top_quantile), returns.loc[date, :], np.nan)
        long_short_returns.loc[date, :] = np.where(long_short_returns.columns.isin(top_half_quantile), returns.loc[date, :], np.nan)
        long_short_returns.loc[date, :] = np.where(long_short_returns.columns.isin(bottom_half_quantile), -returns.loc[date, :], long_short_returns.loc[date, :])

        counter += 1

    return long_only_returns, long_short_returns

def time_series_momentum(df, window_size=252, rebalancing_period=30):
    returns = df.pct_change()
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
        long_short_returns.loc[date, :] = np.where(negative_mean_returns, -returns.loc[date, :], long_short_returns.loc[date, :])

        counter += 1

    return long_only_returns, long_short_returns