import numpy as np

# strategy
def consecutive_strategy_single(historical_stock_data: list, consec_inc: int, consec_dec: int):
    '''consecutive strategy method for a single stock(ticker)
    buy all if the price rises for consec_inc consecutive days
    sell all if the price goes down for consec_dec consecutive days

    Parameter
    historical_stock_data [list]: historical stock price data including today
    consec_inc [int]: consecutive increasing days
    consec_dec [int]: consecutive decreasing days
    '''
    if len(historical_stock_data) > consec_inc:
        if np.all(np.diff(np.array(historical_stock_data[-consec_inc-1:]))>0):
            return 1
    
    if len(historical_stock_data) > consec_dec:
        if np.all(np.diff(np.array(historical_stock_data[-consec_dec-1:]))<0):
            return -1
    
    return 0

def consecutive_strategy(today_stock_data: dict, historical_stock_data: dict, **kwargs):
    '''accumulate consecutive strategy methods for all stocks that have today's data

    Parameter
    today_stock_data [dict]: today stock data to get tradable stocks
    historical_stock_data [dict]: historical price data
    '''
    strategy_vector = []
    for key in today_stock_data.keys():
        strategy_vector.append(consecutive_strategy_single(historical_stock_data[key], **kwargs))
    return strategy_vector
