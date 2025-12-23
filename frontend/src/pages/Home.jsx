import { useEffect, useState } from "react";

import { fetchStocks } from "../api/stocks";
import { fetchHistory } from "../api/history";

import StockCard from "../components/StockCard";
import Modal from "../components/Modal";
import PriceChart from "../components/PriceChart";
import RangeSelector from "../components/RangeSelector";
import PredictPanel from "../components/PredictPanel";


export default function Home() {
  /* =========================
     Global page state
  ========================= */
  const [stocks, setStocks] = useState([]);
  const [loadingStocks, setLoadingStocks] = useState(true);

  const [selectedStock, setSelectedStock] = useState(null);

  /* =========================
     Modal-specific state
  ========================= */
  const [range, setRange] = useState("1mo");
  const [history, setHistory] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(false);

  /* =========================
     Fetch stock list (once)
  ========================= */
  useEffect(() => {
    fetchStocks()
      .then(setStocks)
      .finally(() => setLoadingStocks(false));
  }, []);

  /* =========================
     Fetch history when modal opens
     or range changes
  ========================= */
  useEffect(() => {
    if (!selectedStock) return;

    setLoadingHistory(true);
    setHistory([]);

    fetchHistory(selectedStock.ticker, range)
      .then((data) => {
        console.log("Setting history:", data);
        setHistory(Array.isArray(data) ? data : []);
      })
      .finally(() => setLoadingHistory(false));
  }, [selectedStock, range]);

  /* =========================
     Render
  ========================= */
  if (loadingStocks) {
    return <p className="center">Loading market data…</p>;
  }

  return (
    <div className="container">
      <h1>Market Overview</h1>

      <div className="stock-grid">
        {stocks.map((stock) => (
          <StockCard
            key={stock.ticker}
            ticker={stock.ticker}
            price={stock.last_close}
            onClick={() => {
              setSelectedStock(stock);
              setRange("1mo");      // reset on open
              setHistory([]);
            }}
          />
        ))}
      </div>

      {/* =========================
          Modal
      ========================= */}
      <Modal
        isOpen={!!selectedStock}
        onClose={() => setSelectedStock(null)}
      >
        {selectedStock && (
          <>
            <h2>{selectedStock.ticker}</h2>
            {/* I want to display $ for selected stocks */}
            <p>
              Last Close: {selectedStock.ticker.includes(".NS") ? "₹" : "$"}{" "}
              {Number(selectedStock.last_close).toFixed(2)}
            </p>

            <RangeSelector
              active={range}
              onChange={setRange}
            />

            <div className="chart-container">
              {loadingHistory ? console.log("history", history) : null}
              {loadingHistory ? (
                <p className="chart-placeholder">Loading chart…</p>
              ) : history.length > 0 ? (
                <PriceChart
                  key={`${selectedStock.ticker}-${range}-${history.length}`}
                  data={history}
                  range={range}
                />

              ) : (
                <p>No data available</p>
              )}
              <PredictPanel ticker={selectedStock.ticker} />
            </div>
          </>
        )}
      </Modal>
    </div>
  );
}
