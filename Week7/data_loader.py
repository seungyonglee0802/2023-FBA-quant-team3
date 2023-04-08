import pandas as pd


def load_close():
    # Read the 'clean_ohlcv.csv' file
    clean_ohlcv_df = pd.read_csv("Week7/clean_ohlcv.csv", index_col=0, header=[0, 1])

    # Select the 'CLOSE' column by its position
    close_df = clean_ohlcv_df.iloc[
        :, clean_ohlcv_df.columns.get_level_values(1) == "CLOSE"
    ]
    close_df.columns = close_df.columns.droplevel(1)

    return close_df