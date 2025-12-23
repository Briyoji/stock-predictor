import { useState } from "react";
import { predictNextDay } from "../api/predict";

export default function PredictPanel({ ticker }) {
  const [lookback, setLookback] = useState("short");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handlePredict = async () => {
    setLoading(true);
    setResult(null);

    try {
      const res = await predictNextDay(ticker, lookback);
      setResult(res);
    } catch (err) {
      alert("Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  const direction =
    result && result.predicted_log_return > 0 ? "UP" : "DOWN";

  return (
    <div className="predict-panel">
      <h3>Next-Day Prediction</h3>

      <div className="lookback-selector">
        {["short", "medium", "long"].map((lb) => (
          <button
            key={lb}
            className={lookback === lb ? "active" : ""}
            onClick={() => setLookback(lb)}
          >
            {lb.toUpperCase()}
          </button>
        ))}
      </div>

      <button
        className="predict-btn"
        onClick={handlePredict}
        disabled={loading}
      >
        {loading ? "Predicting…" : "Predict"}
      </button>

      {result && (
        <div className="prediction-result">
          <p>
            <b>Next-Day Log Return:</b>{" "}
            {result.predicted_log_return.toFixed(5)}
          </p>
          <p>
            <b>Direction:</b>{" "}
            <span className={direction.toLowerCase()}>
              {direction}
            </span>
          </p>
          <p>
            <b>Lookback:</b> {result.lookback_window} days
          </p>
        </div>
      )}
    </div>
  );
}
