import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def json_to_df(file_path):
    # Open the JSON file
    with open(file_path, 'r') as file:
        # Load the JSON data
        data = json.load(file)

    # Create a new dictionary with the desired format
    parsed_data = {}
    for key, value in data.items():
        parsed_data[key] = {}
        for inner_key, inner_value in value.items():
            parsed_data[key][inner_value['ISU_SRT_CD']] = int(inner_value['TDD_CLSPRC'].replace(',', ''))

    # Convert the new dictionary to a pandas DataFrame
    df = pd.DataFrame.from_dict(parsed_data, orient='index')

    # Convert the index to datetime format
    df.index = pd.to_datetime(df.index, format='%Y%m%d')

    # Return the DataFrame
    return df

def performance_metrics(returns, risk_free_rate=0.02):
    portfolio_returns = returns.mean(axis=1, skipna=True)
    cumulative_returns = (1 + portfolio_returns).cumprod()
    total_return = cumulative_returns.iloc[-2]
    n = cumulative_returns.count()
    CAGR = (total_return ** (252 / n)) - 1
    volatility = portfolio_returns.std() * np.sqrt(252)
    sharpe_ratio = (CAGR - risk_free_rate) / volatility
    return CAGR, volatility, sharpe_ratio

def get_drawdown(returns):
    portfolio_returns = returns.mean(axis=1, skipna=True)
    cumulative_returns = (1 + portfolio_returns).cumprod()
    peak = cumulative_returns.cummax()
    drawdown = (cumulative_returns - peak) / peak
    return drawdown

def plot_cumulative_return_and_drawdown(returns, title, **kwargs):
    portfolio_returns = returns.mean(axis=1, skipna=True)
    cumulative_returns = (1 + portfolio_returns).cumprod()
    drawdown = get_drawdown(returns)

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 8), gridspec_kw={'height_ratios': [8, 2]})
    fig.suptitle(title, fontsize=16, y=0.98)
    fig.text(0.5, 0.92, f'CAGR: {kwargs.get("cagr"):.2f} Volatility: {kwargs.get("volatility"):.2f} Sharpe Ratio: {kwargs.get("sharpe_ratio"):.2f}', ha='center', fontsize=12)

    ax1.plot(cumulative_returns, label=f'Window Size: {kwargs.get("window_size")}, Quantile: {kwargs.get("quantile")}')
    ax1.set(ylabel='Cumulative Return')
    ax1.legend()

    ax2.plot(drawdown, label=f'Window Size: {kwargs.get("window_size")}, Quantile: {kwargs.get("quantile")}')
    ax2.set(xlabel='Date', ylabel='Drawdown')
    ax2.set_ylim((-1, 0))
    ax2.legend()

    plt.show()