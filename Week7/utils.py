import numpy as np
import matplotlib.pyplot as plt


def performance_metrics(returns, risk_free_rate=0.02):
    cumulative_returns = (1 + returns).cumprod()
    total_return = cumulative_returns.iloc[-2]
    n = cumulative_returns.count()
    CAGR = (total_return ** (252 / n)) - 1
    volatility = returns.std() * np.sqrt(252)
    sharpe_ratio = (CAGR - risk_free_rate) / volatility
    return CAGR, volatility, sharpe_ratio


def get_drawdown(returns):
    cumulative_returns = (1 + returns).cumprod()
    peak = cumulative_returns.cummax()
    drawdown = (cumulative_returns - peak) / peak
    return drawdown


def plot_cumulative_return_and_drawdown(returns, title, **kwargs):
    CAGR, volatility, sharpe_ratio = performance_metrics(returns)
    drawdown = get_drawdown(returns)
    cumulative_returns = (1 + returns).cumprod()

    fig, (ax1, ax2) = plt.subplots(
        2, 1, sharex=True, figsize=(10, 8), gridspec_kw={"height_ratios": [8, 2]}
    )
    fig.suptitle(title, fontsize=16, y=0.98)
    fig.text(
        0.5,
        0.92,
        f"CAGR: {CAGR:.2f} Volatility: {volatility:.2f} Sharpe Ratio: {sharpe_ratio:.2f}",
        ha="center",
        fontsize=12,
    )

    ax1.plot(
        cumulative_returns,
        label=f'Window Size: {kwargs.get("window_size")}, Quantile: {kwargs.get("quantile")}, Rebalancing Period: {kwargs.get("rebalancing_period")}',
    )
    ax1.set(ylabel="Cumulative Return")
    ax1.legend()

    ax2.plot(
        drawdown,
        label=f'Window Size: {kwargs.get("window_size")}, Quantile: {kwargs.get("quantile")}, Rebalancing Period: {kwargs.get("rebalancing_period")}',
    )
    ax2.set(xlabel="Date", ylabel="Drawdown")
    ax2.set_ylim((-1, 0))
    ax2.legend()

    plt.show()
