import torch
import torch.nn as nn

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")  # macbook


class LSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim, dropout):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.lstm = nn.LSTM(
            input_dim, hidden_dim, num_layers, batch_first=True, dropout=dropout
        )
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        h0 = (
            torch.zeros(self.num_layers, x.size(0), self.hidden_dim)
            .requires_grad_()
            .to(device)
        )
        c0 = (
            torch.zeros(self.num_layers, x.size(0), self.hidden_dim)
            .requires_grad_()
            .to(device)
        )
        out, _ = self.lstm(x, (h0.detach(), c0.detach()))
        out = self.fc(out[:, -1, :])
        return out
