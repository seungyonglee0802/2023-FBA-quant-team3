import numpy as np
import matplotlib.pyplot as plt
import torch
from tqdm import tqdm

from dataloader import get_dataloader
from util import get_data, get_normalized_data, split_trn_eval, calculate_accuracy

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")  # macbook


def train(epochs, model, trn_loader, criterion, optimizer):
    pbar = tqdm(range(epochs))
    total_loss = []
    for epoch in pbar:
        for seq, labels in trn_loader:
            seq = seq.to(device)
            labels = labels.to(device)
            optimizer.zero_grad()
            y_pred = model(seq)
            loss = criterion(y_pred, labels)
            loss.backward()
            optimizer.step()
            total_loss.append(loss.item())
        pbar.set_postfix(loss=np.mean(total_loss))


def eval(model, evl_loader):
    model.eval()
    with torch.no_grad():
        preds = []
        labels = []
        for seq, label in evl_loader:
            seq = seq.to(device)
            label = label.to(device)
            y_pred = model(seq)
            preds.append(y_pred.item())
            labels.append(label.item())
    return preds, labels


def forcast(model, train_data, seq_len, future_day, minmax):
    model.eval()

    output_predict = np.zeros((train_data.shape[0] + future_day, train_data.shape[1]))
    output_predict[:seq_len] = train_data[:seq_len]

    for k in range(train_data.shape[0] - seq_len):
        out_logits = model(
            torch.Tensor(train_data[k : k + seq_len]).unsqueeze(0).to(device)
        )
        output_predict[k + seq_len] = out_logits.detach().numpy()

    for i in range(future_day):
        o = output_predict[-future_day - seq_len + i : -future_day + i]
        out_logits = model(torch.Tensor(o).unsqueeze(0).to(device))
        output_predict[-future_day + i] = out_logits.detach().numpy()

    unnormalized_output_predict = minmax.inverse_transform(output_predict)

    return unnormalized_output_predict


def plot_prediction(target, predict, trn_size=None):
    # accuracies = calculate_accuracy(target[-test_size:], predict[-test_size:])

    plt.figure(figsize=(15, 5))
    plt.plot(target, label="true trend", c="black")
    plt.plot(predict, label="predicted trend", c="green")
    if trn_size:
        # plot vertical line as the last position of training set
        plt.vlines(
            x=trn_size,
            ymin=np.min(target),
            ymax=np.max(target),
            linestyles="--",
            colors="red",
            label="Last training day",
        )
    plt.legend()
    # plt.title(f'KOSPI trend prediction {accuracies:.2f}')
    plt.show()


def main(model, args):
    # Hyperparameters
    seq_len = args.seq_len
    batch_size = args.batch_size
    learning_rate = args.learning_rate
    epochs = args.epochs
    future_day = args.future_day

    # Data
    df = get_data(args.data_path)
    normalized_adj_close, unnomalized_adj_close, minmax = get_normalized_data(
        df, 1
    )  # Adj Close in column 1
    trn_data, evl_data = split_trn_eval(normalized_adj_close, 0.9)
    trn_loader = get_dataloader(trn_data, seq_len, batch_size)
    evl_loader = get_dataloader(evl_data, seq_len, batch_size=1, shuffle=False)

    # Model
    # model = LSTM(input_dim=1, hidden_dim=hidden_dim, num_layers=num_layers, output_dim=1).to(device)
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # Train
    train(epochs, model, trn_loader, criterion, optimizer)

    # Evaluate
    preds, labels = eval(model, evl_loader)
    print(f"Accuracy: {calculate_accuracy(labels, preds):.2f}")

    # Forcast
    unnormalized_output_predict = forcast(model, trn_data, seq_len, future_day, minmax)
    plot_prediction(
        unnomalized_adj_close, unnormalized_output_predict, trn_size=len(trn_data)
    )


if __name__ == "__main__":
    # argparse
    import argparse

    argparser = argparse.ArgumentParser()
    argparser.add_argument("model", type=str, choices=["lstm", "transformer"])
    argparser.add_argument("--data_path", type=str, default="dataset/pp_kospi.csv")
    argparser.add_argument("--epochs", type=int, default=50)
    argparser.add_argument("--batch_size", type=int, default=32)
    argparser.add_argument("--hidden_dim", type=int, default=64)
    argparser.add_argument("--learning_rate", type=float, default=0.001)
    argparser.add_argument("--seq_len", type=int, default=20)
    argparser.add_argument("--future_day", type=int, default=100)
    argparser.add_argument("--num_layers", type=int, default=2)
    argparser.add_argument("--dropout", type=float, default=0.5)
    # only for transformer
    argparser.add_argument("--nhead", type=int, default=8)
    args = argparser.parse_args()

    if args.model == "lstm":
        from model.lstm import LSTM

        model = LSTM(
            input_dim=1,
            hidden_dim=args.hidden_dim,
            num_layers=args.num_layers,
            output_dim=1,
            dropout=args.dropout,
        ).to(device)

    elif args.model == "transformer":
        from model.transformer import Transformer

        model = Transformer(
            hidden_dim=args.hidden_dim,
            num_layers=args.num_layers,
            nhead=args.nhead,
            dropout=args.dropout,
        ).to(device)

    main(model, args)
