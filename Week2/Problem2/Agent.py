import pandas as pd

class Agent:

    def __init__ (self, name="The agent"):
        '''create a agent with given name having $1000
        
        Arguments
        name [str]: name of the agent (default: The agent)
        '''
        self._name = name
        self._credit = 1000
        self._holdings = pd.DataFrame(index=["avg_price", "num"], dtype="float")
        self._stock_data = {}
        self._today_stock_data = {}

        print(f"{self._name} is created.")

    def check(self):
    
        '''print current state(credit and holdings) of the agent
        '''
        print(f"credit : {self._credit}")
        print(f"holding : {self.df_to_list(self._holdings)}")
    
    def recieve_stock_data(self, new_stock_data: list):
        '''update self._stock_data DataFrame from given new_stock_data

        Arguments
        new_stock_data [list(list(str, float))]: i.e., [["APPL", 143.1], ["GOOGL", 500.2]]
        '''
        self.update_stock_data(new_stock_data)
        self._today_stock_data = dict(new_stock_data)

    def buy(self, buy_inform : list):
        '''buy stocks according to buy_inform

        Arguments
        buy_inform [list]: information of the stock to buy [ticker : str, price : float|int, quantity : int]
        '''
        ticker, price, quantity = buy_inform

        if not quantity > 0:
            return

        if price*quantity > self._credit:
            print(f"{self._name} can't buy.")
            return
        
        if ticker in self._holdings.columns:
            ticker_holdings = self._holdings[ticker]
            prev_avg_price = ticker_holdings["avg_price"]
            prev_num = ticker_holdings["num"]
            ticker_holdings["avg_price"] = (prev_avg_price*prev_num + price*quantity)/(prev_num + quantity)
            ticker_holdings["num"] += quantity
        else:
            self._holdings[ticker] = [price, quantity]

        self._credit -= price*quantity

        print(f"{self._name} buys {int(quantity)} {ticker} for {price}.")
        return

    def sell(self, sell_inform : list):
        '''sell stocks according to sell_inform

        Arguments
        sell_inform [list]: information of the stock to sell [ticker : str, price : float|int, quantity : int]
        '''
        ticker, price, quantity = sell_inform

        if not quantity > 0:
            return

        if not ticker in self._holdings.columns or quantity > self._holdings[ticker]["num"]:
            print(f"{self._name} can't sell.")
            return
        
        ticker_holdings = self._holdings[ticker]
        ticker_holdings["num"] -= quantity
        if ticker_holdings["num"] == 0:
            self._holdings.drop(columns=[ticker], inplace=True)
        self._credit += price*quantity

        print(f"{self._name} sells {int(quantity)} {ticker} for {price}.")
        return

    def trading(self, strategy, **kwargs):
        '''trade w.r.t given strategy
        strategy can get arguments by kwargs

        Parameters
        strategy [func]: function that return a normalized vector that indicates
        to buy or sell each stock
        '''
        strategy_result = strategy(self._today_stock_data, self._stock_data, **kwargs)
        assert len(self._stock_data.keys()) == len(strategy_result)

        for ticker, order in zip(self._stock_data.keys(), strategy_result):
            if order == 1:
                price = self._today_stock_data[ticker]
                max_quantity = self._credit // price
                if max_quantity > 0:
                    self.buy([ticker, price, max_quantity])
                    return ticker, "buy", price, max_quantity
            elif order == -1 and ticker in self._holdings:
                price = self._today_stock_data[ticker]
                max_quantity = self._holdings[ticker]["num"]
                if max_quantity > 0:
                    self.sell([ticker, price, max_quantity])
                    return ticker, "sell", price, max_quantity
            else:
                pass
        
        return None

    def update_stock_data(self, new_stock_data):
        '''update _stock_data [dict] w.r.t new_stock_data

        Parameters
        new_stock_data [list]: [list(list(str, float))]: i.e., [["APPL", 143.1], ["GOOGL", 500.2]]
        '''
        for ticker, price in new_stock_data:
            if ticker in self._stock_data.keys():
                self._stock_data[ticker].append(price)
            else:
                self._stock_data[ticker] = [price]
    
    def df_to_list(self, df: pd.DataFrame):
        '''convert dataframe object to list

        Arguments
        df [pd.DataFrame]: DataFrame of holdings (index: avg_price, num; columns: tickers)
        '''
        return [[ticker] + df[ticker].tolist() for ticker in df.columns]