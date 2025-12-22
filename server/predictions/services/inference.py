import numpy as np
import torch
import joblib
from ml.training.lstm import LSTMModel

from ml import MODELS_DIR

MODEL_REGISTRY = {
    "short": {"model_path": MODELS_DIR / "short/model.pt", "scaler_path": MODELS_DIR / "short/scaler_short.pkl", "version": "lstm_short_v1"},
    "medium": {"model_path": MODELS_DIR / "medium/model.pt", "scaler_path": MODELS_DIR / "medium/scaler_medium.pkl", "version": "lstm_medium_v1"},
    "long": {"model_path": MODELS_DIR / "long/model.pt", "scaler_path": MODELS_DIR / "long/scaler_long.pkl", "version": "lstm_long_v1"},
}


_MODEL_CACHE = {}
_SCALER_CACHE = {}


def load_model(path, input_size):
    model = LSTMModel(num_features=input_size)
    model.load_state_dict(torch.load(path, map_location="cpu"))
    model.eval()
    return model


def get_model(lookback, input_size):
    if lookback not in _MODEL_CACHE:
        path, version = MODEL_REGISTRY[lookback]
        model = load_model(path, input_size)
        _MODEL_CACHE[lookback] = (model, version)
    return _MODEL_CACHE[lookback]


@torch.no_grad()
def run_inference(features, lookback):
    # features: (seq_len, num_features)
    # input_size = features.shape[1]

    # model, version = get_model(lookback, input_size)

    # X = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
    # prediction = model(X).item()

    # return prediction, version

    config = MODEL_REGISTRY[lookback]

    if lookback not in _MODEL_CACHE and lookback not in _SCALER_CACHE:
        model = load_model(config["model_path"], input_size=features.shape[1])
        scaler = joblib.load(config["scaler_path"])

        _MODEL_CACHE[lookback] = model
        _SCALER_CACHE[lookback] = scaler

    model = _MODEL_CACHE[lookback]
    scaler = _SCALER_CACHE[lookback]

    # IMPORTANT: transform, not fit
    features_scaled = scaler.transform(features)

    X = torch.tensor(features_scaled, dtype=torch.float32).unsqueeze(0)
    prediction = model(X).item()

    return prediction, config["version"]
