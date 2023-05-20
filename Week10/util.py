import pandas as pd
import torch
from sklearn.preprocessing import MinMaxScaler


def get_data(dir):
    df = pd.read_csv(dir)
    df = df.dropna()
    df = df.reset_index(drop=True)
    return df


def get_normalized_data(df, idx):
    df_adj_close = df.iloc[:, idx : idx + 1].astype("float32")
    minmax = MinMaxScaler().fit(df_adj_close)  # Adj Close MinMaxScaler
    normalized_adj_close = minmax.transform(
        df_adj_close
    )  # Normalized Adj Close (np.array)
    return normalized_adj_close, df_adj_close.to_numpy(), minmax


def split_trn_eval(data_arr, trn_size=0.8):
    trn_data = data_arr[: int(len(data_arr) * trn_size)]
    eval_data = data_arr[int(len(data_arr) * trn_size) :]
    return trn_data, eval_data


def calculate_accuracy(real, predict):
    real = torch.tensor(real) + 1
    predict = torch.tensor(predict) + 1
    percentage = 1 - torch.sqrt(torch.mean(torch.square((real - predict) / real)))
    return percentage * 100
