# lstm.py

import torch
import torch.nn as nn


class LSTMModel(nn.Module):
    def __init__(self, num_features: int, hidden_size: int = 32):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=num_features,
            hidden_size=hidden_size,
            batch_first=True,
        )
        self.dropout = nn.Dropout(0.2)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        # x: (batch, lookback, features)
        out, _ = self.lstm(x)
        out = out[:, -1, :]      # last timestep
        out = self.dropout(out)
        out = self.fc(out)
        return out.squeeze(-1)
