import pandas as pd
import torch
from sklearn.preprocessing import MinMaxScaler


def get_data(dir):
    df = pd.read_csv(dir)
    df = df.dropna(axis=1)
    df = df.reset_index(drop=True)
    return df


def get_normalized_KOSPI(df, idx=1):
    df_adj_close = df.iloc[:, idx : idx + 1].astype("float32")
    minmax = MinMaxScaler().fit(df_adj_close)  # Adj Close MinMaxScaler
    normalized_adj_close = minmax.transform(
        df_adj_close
    )  # Normalized Adj Close (np.array)
    return normalized_adj_close, df_adj_close.to_numpy(), minmax


def get_normalized_data(df):
    df = df.iloc[:, 1:].astype("float32")
    df_transposed = df.transpose()
    numpy_array = df_transposed.values
    minmax = MinMaxScaler().fit(numpy_array)
    normalized_data = minmax.transform(numpy_array)
    return normalized_data


def split_trn_eval(data_arr, trn_size=0.8):
    trn_data = data_arr[: int(len(data_arr) * trn_size)]
    eval_data = data_arr[int(len(data_arr) * trn_size) :]
    return trn_data, eval_data


def calculate_accuracy(real, predict):
    real = torch.tensor(real) + 1
    predict = torch.tensor(predict) + 1
    percentage = 1 - torch.sqrt(torch.mean(torch.square((real - predict) / real)))
    return percentage * 100
