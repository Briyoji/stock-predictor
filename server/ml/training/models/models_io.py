# model_io.py

import torch
import json
from pathlib import Path
from datetime import datetime


def save_model(
    model,
    model_dir: str,
    metadata: dict,
):
    model_dir = Path(model_dir)
    model_dir.mkdir(parents=True, exist_ok=True)

    # Save weights
    torch.save(model.state_dict(), model_dir / "model.pt")

    # Add timestamp
    metadata["saved_at"] = datetime.utcnow().isoformat()

    # Save metadata
    with open(model_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
        

def load_model(model_class, model_dir: str, device="cpu"):
    model_dir = Path(model_dir)

    with open(model_dir / "metadata.json") as f:
        metadata = json.load(f)

    model = model_class(
        num_features=metadata["num_features"],
        hidden_size=metadata["hidden_size"],
    )

    model.load_state_dict(
        torch.load(model_dir / "model.pt", map_location=device)
    )

    model.eval()
    return model, metadata
