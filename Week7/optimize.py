import itertools
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
from backtest import backtest_daily
from momentum import cross_sectional_momentum, time_series_momentum
from utils import performance_metrics
from data_loader import load_close


def find_best_parameters(
    df, momentum_type, trade_type, window_sizes, rebalancing_periods
):
    best_sharpe_ratio = -np.inf
    sharpe_ratios = {}

    for window_size, rebalancing_period in itertools.product(
        window_sizes, rebalancing_periods
    ):
        if momentum_type == "cross_sectional":
            long_only_signal, long_short_signal = cross_sectional_momentum(
                df, window_size=window_size, rebalancing_period=rebalancing_period
            )
        elif momentum_type == "time_series":
            long_only_signal, long_short_signal = time_series_momentum(
                df, window_size=window_size, rebalancing_period=rebalancing_period
            )
        else:
            raise ValueError(f"Invalid momentum type: {momentum_type}")

        if trade_type == "long_only":
            strategy_returns = backtest_daily(df, long_only_signal)
            _, _, sharpe_ratio = performance_metrics(strategy_returns)
        elif trade_type == "long_short":
            strategy_returns = backtest_daily(df, long_short_signal)
            _, _, sharpe_ratio = performance_metrics(strategy_returns)

        sharpe_ratios[(window_size, rebalancing_period)] = sharpe_ratio

        if sharpe_ratio > best_sharpe_ratio:
            best_sharpe_ratio = sharpe_ratio
            best_window_size = window_size
            best_rebalancing_period = rebalancing_period

    print(
        f"Best Sharpe ratio: {best_sharpe_ratio:.2f} (window size = {best_window_size}, rebalacing period = {best_rebalancing_period})"
    )

    return sharpe_ratios


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find the best parameters for a momentum-based trading strategy"
    )
    parser.add_argument(
        "--trade_type",
        type=str,
        default="long_only",
        choices=["long_only", "long_short"],
        help="Type of trading strategy",
    )
    parser.add_argument(
        "--momentum_type",
        type=str,
        default="cross_sectional",
        choices=["cross_sectional", "time_series"],
        help="Type of momentum strategy",
    )
    parser.add_argument(
        "--window_sizes",
        type=int,
        nargs="+",
        default=[63, 126, 189, 252, 315, 378, 441, 504],
        help="List of window sizes to test",
    )
    parser.add_argument(
        "--rebalancing_periods",
        type=int,
        nargs="+",
        default=[5, 10, 21, 42, 63],
        help="List of rebalancing periods to test",
    )

    args = parser.parse_args()

    close_df = load_close()
    # call find_best_parameters() with the parsed arguments
    sharpe_ratios = find_best_parameters(
        close_df,
        trade_type=args.trade_type,
        momentum_type=args.momentum_type,
        window_sizes=args.window_sizes,
        rebalancing_periods=args.rebalancing_periods,
    )

    # Plot the results as a heatmap
    sharpe_ratio_grid = np.zeros(
        (len(args.window_sizes), len(args.rebalancing_periods))
    )
    for i, window_size in enumerate(args.window_sizes):
        for j, rebalancing_period in enumerate(args.rebalancing_periods):
            sharpe_ratio_grid[i, j] = sharpe_ratios[(window_size, rebalancing_period)]

    plt.figure(figsize=(8, 6))
    sns.heatmap(
        sharpe_ratio_grid,
        cmap="RdYlGn",
        annot=True,
        fmt=".2f",
        xticklabels=args.rebalancing_periods,
        yticklabels=args.window_sizes,
    )
    plt.xlabel("Rebalancing Period")
    plt.ylabel("Window Size")
    plt.title(f"Sharpe Ratio Grid for {args.momentum_type} {args.trade_type} Strategy")
    plt.show()
