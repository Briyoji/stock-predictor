# Stock Predictor — Django + ML System

This project is a full-stack machine learning system for predicting **next-day stock price movement** using historical market data from Yahoo Finance.  
It is designed as a **production-style ML application**, not a trading bot or financial advisory tool.

---

## 🎯 Project Objective

- Predict the **next trading day’s log return** for a given stock
- Support multiple historical contexts (short / medium / long lookback)
- Expose predictions via a REST API
- Maintain strict separation between training and inference

---

## 🧱 System Architecture

The system is decomposed into four independent layers:

1. **Frontend**
   - Consumes REST APIs
   - Allows users to select ticker and context (short / medium / long)
   - Displays historical prices and predicted output

2. **Backend (Django + DRF)**
   - Orchestrates requests
   - Routes inference calls
   - Persists predictions and metadata
   - Does NOT train models

3. **ML Layer (Offline)**
   - Data collection and feature engineering
   - Model training and evaluation
   - Versioned artifact generation

4. **Database**
   - Stores stock metadata
   - Stores prediction results
   - Does NOT store raw Yahoo Finance dumps

---

## 📈 Prediction Design

- **Forecast Horizon:** 1 trading day ahead (single-step forecasting)
- **Target Variable:** Next-day log return  
  \[
  r_{t+1} = \log\left(\frac{P_{t+1}}{P_t}\right)
  \]
  

### User Context Options

| Context | Lookback Window | Interpretation |
|-------|----------------|----------------|
| Short | 20 trading days | Momentum / noise |
| Medium | 60 trading days | Trend |
| Long | 120 trading days | Regime context |

⚠️ The lookback window changes the **historical context**, not the prediction horizon.

---

## 🧠 Modeling Strategy

- Separate LSTM models per lookback window
- Same target and loss function across all models
- Training is:
  - Offline
  - Reproducible
  - Versioned
- Inference is:
  - Stateless
  - Read-only
  - Cached where appropriate

### Baselines
Each model is evaluated against:
- Naïve last-day predictor
- Moving average predictor
- ARIMA (optional)

---

## 📂 Project Structure
```
stock-predictor/
├── backend/          # Django backend (API + orchestration)
├── ml/               # Offline ML training and evaluation
├── scripts/          # Setup and automation scripts
├── README.md
├── .gitignore
└── pyproject.toml
```
---

## ⚙️ Environment Management

- Python environment managed using **uv**
- Dependencies declared in `pyproject.toml`
- Run all commands using `uv run ...`

---

## 🚀 Getting Started

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Run Django migrations:

   ```bash
   uv run python backend/manage.py migrate
   ```

3. Start the development server:

   ```bash
   uv run python backend/manage.py runserver
   ```

---

## ⚠️ Disclaimer

This project is for **educational and system-design purposes only**.
It is **not** intended for trading, investment decisions, or financial advice.

---

## 📌 Design Philosophy

* Clear separation of concerns
* No data leakage
* Time-based evaluation only
* Simplicity over unnecessary complexity
* Explainable and defensible ML decisions
