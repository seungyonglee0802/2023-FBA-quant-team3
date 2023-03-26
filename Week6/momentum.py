import numpy as np

def cross_sectional_momentum(df, window_size=252, quantile=0.1):
    returns = df.pct_change()
    momentum = df.apply(lambda x: x / x.shift(window_size) - 1)

    long_only = returns.copy()
    long_short = returns.copy()

    for date, row in momentum.iterrows():

        # Get top and bottom quantile index of momentum
        n = int(len(row) * quantile)
        top_quantile = row.nlargest(n).index if sum(~row.isna()) >= n else []
        top_half_quantile = row.nlargest(n//2).index if sum(~row.isna()) >= n else []
        bottom_half_quantile = row.nsmallest(n//2).index if sum(~row.isna()) >= n else []

        long_only.loc[date, :] = np.where(long_only.columns.isin(top_quantile), returns.loc[date, :], 0)
        long_short.loc[date, :] = np.where(long_short.columns.isin(top_half_quantile), returns.loc[date, :], 0)
        long_short.loc[date, :] = np.where(long_short.columns.isin(bottom_half_quantile), -returns.loc[date, :], long_short.loc[date, :])

    return long_only, long_short

def time_series_momentum(df, window_size=252):
    returns = df.pct_change()
    rolling_mean = returns.rolling(window=window_size).mean()

    long_only = returns.copy()
    long_short = returns.copy()

    for date, row in rolling_mean.iterrows():
        long_only.loc[date, :] = np.where(row > 0, returns.loc[date, :], 0)
        long_short.loc[date, :] = np.where(row > 0, returns.loc[date, :], 0)
        long_short.loc[date, :] = np.where(row < 0, -returns.loc[date, :], long_short.loc[date, :])

    return long_only, long_short