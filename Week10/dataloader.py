from torch.utils.data import Dataset, ConcatDataset, DataLoader


class StockDataset(Dataset):
    def __init__(self, data, seq_len):
        self.data = data
        self.seq_len = seq_len

    def __len__(self):
        return len(self.data) - self.seq_len

    def __getitem__(self, idx):
        return self.data[idx : idx + self.seq_len], self.data[idx + self.seq_len]


def get_dataloader(data, seq_len, batch_size, shuffle=True):
    num_stocks = data.shape[0]
    datasets = [StockDataset(data[i], seq_len) for i in range(num_stocks)]
    dataset = ConcatDataset(datasets)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
    return dataloader
