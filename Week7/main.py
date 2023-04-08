import pandas as pd
import argparse
from momentum import cross_sectional_momentum, time_series_momentum
from backtest import backtest_daily
from utils import plot_cumulative_return_and_drawdown


def plot_cross_sectional_momentum(
    close_df, window_size=252, quantile=0.1, rebalancing_period=21, **kwargs
):
    # get signal
    long_only_signal, long_short_signal = cross_sectional_momentum(
        close_df,
        window_size=window_size,
        quantile=quantile,
        rebalancing_period=rebalancing_period,
    )

    # backtest and plot
    strategy_returns = backtest_daily(close_df, long_only_signal)
    plot_cumulative_return_and_drawdown(
        strategy_returns,
        "Cross-sectional Momentum Long Only Strategy",
        window_size=window_size,
        quantile=quantile,
        rebalancing_period=rebalancing_period,
    )

    strategy_returns = backtest_daily(close_df, long_short_signal)
    plot_cumulative_return_and_drawdown(
        strategy_returns,
        "Cross-sectional Momentum Long Short Strategy",
        window_size=window_size,
        quantile=quantile,
        rebalancing_period=rebalancing_period,
    )


def plot_time_series_momentum(
    close_df, window_size=252, rebalancing_period=21, **kwargs
):
    # get signal
    long_only_signal, long_short_signal = time_series_momentum(
        close_df, window_size=window_size, rebalancing_period=rebalancing_period
    )

    # backtest and plot
    strategy_returns = backtest_daily(close_df, long_only_signal)
    plot_cumulative_return_and_drawdown(
        strategy_returns,
        "Time-series Momentum Long Only Strategy",
        window_size=window_size,
        rebalancing_period=rebalancing_period,
    )

    strategy_returns = backtest_daily(close_df, long_short_signal)
    plot_cumulative_return_and_drawdown(
        strategy_returns,
        "Time-series Momentum Long Short Strategy",
        window_size=window_size,
        rebalancing_period=rebalancing_period,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-M", "--momentum_type", type=str, default="cross_sectional")
    parser.add_argument("-W", "--window_size", type=int, default=252)
    parser.add_argument("-Q", "--quantile", type=float, default=0.1)
    parser.add_argument("-RE", "--rebalancing_period", type=int, default=21)
    args = parser.parse_args()

    # Read the 'clean_ohlcv.csv' file
    clean_ohlcv_df = pd.read_csv("Week7/clean_ohlcv.csv", index_col=0, header=[0, 1])

    # Select the 'CLOSE' column by its position
    close_df = clean_ohlcv_df.iloc[
        :, clean_ohlcv_df.columns.get_level_values(1) == "CLOSE"
    ]
    close_df.columns = close_df.columns.droplevel(1)

    if args.momentum_type == "cross_sectional":
        plot_cross_sectional_momentum(
            close_df,
            window_size=args.window_size,
            quantile=args.quantile,
            rebalancing_period=args.rebalancing_period,
        )
    elif args.momentum_type == "time_series":
        plot_time_series_momentum(
            close_df,
            window_size=args.window_size,
            rebalancing_period=args.rebalancing_period,
        )
    else:
        raise ValueError(f"Invalid momentum type: {args.momentum_type}")
