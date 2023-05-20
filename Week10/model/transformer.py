import torch.nn as nn


class Transformer(nn.Module):
    def __init__(
        self,
        hidden_dim: int = 512,
        num_layers: int = 1,
        nhead: int = 8,
        dropout: float = 0.1,
    ):
        super(Transformer, self).__init__()
        self.encoder = nn.Linear(1, hidden_dim)
        self.encoder_layer = nn.TransformerEncoderLayer(
            d_model=hidden_dim, nhead=nhead, dropout=dropout, batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(
            self.encoder_layer, num_layers=num_layers
        )
        self.decoder = nn.Linear(hidden_dim, 1)

    def forward(self, src):
        src = self.encoder(src)
        output = self.transformer_encoder(src)
        return self.decoder(
            output[:, -1, :]
        )  # return only the output of the last prediction
