# train_lstm.py

from .lstm import LSTMModel
from ml.baselines.metrics import rmse
# from .models import save_model, load_model

import torch
from torch.utils.data import TensorDataset, DataLoader
import numpy as np


def train_lstm(
    X_train, y_train,
    X_val, y_val,
    num_epochs=50,
    batch_size=64,
    lr=1e-3,
):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    X_train_t = torch.tensor(X_train, dtype=torch.float32)
    y_train_t = torch.tensor(y_train, dtype=torch.float32)
    X_val_t = torch.tensor(X_val, dtype=torch.float32)
    y_val_t = torch.tensor(y_val, dtype=torch.float32)

    train_loader = DataLoader(
        TensorDataset(X_train_t, y_train_t),
        batch_size=batch_size,
        shuffle=False,   # IMPORTANT: no shuffling for time series
    )

    model = LSTMModel(num_features=X_train.shape[2]).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = torch.nn.MSELoss()

    best_val = float("inf")
    patience = 15
    patience_ctr = 0
    best_state = None

    for epoch in range(num_epochs):
        model.train()
        for xb, yb in train_loader:
            xb, yb = xb.to(device), yb.to(device)
            optimizer.zero_grad()
            preds = model(xb)
            loss = loss_fn(preds, yb)
            loss.backward()
            optimizer.step()

        model.eval()
        with torch.no_grad():
            val_preds = model(X_val_t.to(device))
            val_loss = loss_fn(val_preds, y_val_t.to(device)).item()

        print(f"Epoch {epoch+1:02d} | Val MSE: {val_loss:.6f}")

        if val_loss < best_val:
            best_val = val_loss
            best_state = model.state_dict()
            patience_ctr = 0
        else:
            patience_ctr += 1
            if patience_ctr >= patience:
                print("Early stopping.")
                break

    model.load_state_dict(best_state)
    return model

def evaluate(model, X_test, y_test):
    device = next(model.parameters()).device
    model.eval()

    X_test_t = torch.tensor(X_test, dtype=torch.float32).to(device)
    with torch.no_grad():
        preds = model(X_test_t).cpu().numpy()

    return rmse(y_test, preds)

