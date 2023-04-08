import pandas as pd
import glob

# Create a list of CSV files to read
csv_files = glob.glob("Week7/data/*.csv")

# Create an empty dictionary to store dataframes
dfs = {}

# Read each CSV file and add to the dictionary
for i, csv_file in enumerate(csv_files):
    column_name = csv_file.split("/")[-1].split(".")[0].split("_")[-1].upper()
    df = pd.read_csv(csv_file, index_col=0)
    if column_name == "OPEN":
        open_date = df.index
    if column_name == "TRDABLE":
        # Replace '정상' with True and NaN with False
        df = df.replace("정상", True).replace("정지", False).fillna(False)
        df = df.reindex(open_date).fillna(method="ffill")
    stock_code = df.columns
    df.columns = pd.MultiIndex.from_product([stock_code, [column_name]])
    dfs[i] = df

# Concatenate all dataframes into a single dataframe
combined_df = pd.concat(dfs.values(), axis=1)

# Sort the columns in multi-level format
combined_df = combined_df.sort_index(axis=1)

# Change the order of the low-level columns
column_order = ["OPEN", "HIGH", "LOW", "CLOSE", "VOL", "SHARES", "TRDABLE"]
combined_df = combined_df.reindex(columns=column_order, level=1)

# Save the dataframe as a CSV file
combined_df.to_csv("Week7/clean_ohlcv.csv")
