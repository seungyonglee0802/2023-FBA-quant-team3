import argparse
import pandas as pd

from Agent import Agent
from strategy import consecutive_strategy
from utils import save_as_csv

# read stock_data.csv by config
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="input data")
    parser.add_argument("-d", "--cost-data", type=str, help="Enter csv file name")
    
    args = parser.parse_args()

    stock_data_df = pd.read_csv(args.cost_data, index_col=0, delimiter=", ", engine='python')

FBA_agent = Agent("FBA_agent")

# send daily stock price to the agent
# when get return from agent, log it in log_data
log_data = []

tickers = stock_data_df.columns
for idx in stock_data_df.index:
    # stock_data = list(stock_data)
    FBA_agent.recieve_stock_data([[ticker, price] for ticker, price in zip(tickers, stock_data_df.loc[idx])])
    trading_log = FBA_agent.trading(consecutive_strategy, consec_inc=2, consec_dec=1)
    if trading_log: log_data.append(trading_log)

# turn log_data to log_data.csv and save it
save_as_csv("log_data.csv", log_data)