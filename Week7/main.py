import argparse
from momentum import cross_sectional_momentum, time_series_momentum
from backtest import backtest_daily
from utils import plot_cumulative_return_and_drawdown
from data_loader import load_close


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
    strategy_returns, benchmark_returns = backtest_daily(close_df, long_only_signal)
    plot_cumulative_return_and_drawdown(
        strategy_returns,
        benchmark_returns,
        "Cross-sectional Momentum Long Only Strategy",
        list(long_only_signal.keys()),
        window_size=window_size,
        quantile=quantile,
        rebalancing_period=rebalancing_period,
    )

    strategy_returns, benchmark_returns = backtest_daily(close_df, long_short_signal)
    plot_cumulative_return_and_drawdown(
        strategy_returns,
        benchmark_returns,
        "Cross-sectional Momentum Long Short Strategy",
        list(long_short_signal.keys()),
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
        list(long_only_signal.keys()),
        window_size=window_size,
        rebalancing_period=rebalancing_period,
    )

    strategy_returns = backtest_daily(close_df, long_short_signal)
    plot_cumulative_return_and_drawdown(
        strategy_returns,
        "Time-series Momentum Long Short Strategy",
        list(long_short_signal.keys()),
        window_size=window_size,
        rebalancing_period=rebalancing_period,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-M",
        "--momentum_type",
        type=str,
        default="cross_sectional",
        choices=["cross_sectional", "time_series"],
    )
    parser.add_argument("-W", "--window_size", type=int, default=252)
    parser.add_argument("-Q", "--quantile", type=float, default=0.1)
    parser.add_argument("-RE", "--rebalancing_period", type=int, default=21)
    args = parser.parse_args()

    close_df = load_close()

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
