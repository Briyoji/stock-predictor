from ml import load_dataset, TICKERS, MODELS_DIR

from .train_lstm import train_lstm, evaluate
from .models.models_io import save_model

def run_model_building():
    dataset_horizons = [
        ("short", 120, 128, 20), 
        ("medium", 120, 128, 60), 
        ("long", 120, 128, 120),
    ]

    for dataset_horizon, num_epoch, batch_size, lookback_period in dataset_horizons:
        print(f"Training and evaluating for dataset horizon: {dataset_horizon}")
        (train, val, test) = load_dataset(f"{dataset_horizon}")
        X_train, y_train = train
        X_val, y_val = val
        X_test, y_test = test

        model = train_lstm(X_train, y_train, X_val, y_val, num_epoch, batch_size)
        test_rmse = evaluate(model, X_test, y_test)

        save_model(
            model,
            model_dir= MODELS_DIR / dataset_horizon,
            metadata={
                "horizon": dataset_horizon,
                "lookback": lookback_period,
                "num_features": X_train.shape[2],
                "hidden_size": 32,
                "test_rmse": test_rmse,
                "scaler": f"scalers/scaler_{dataset_horizon}.pkl",
                "tickers": TICKERS,
            },
        )

        print("LSTM Test RMSE:", test_rmse, end="\n\n")

if __name__ == "__main__":
    run_model_building()