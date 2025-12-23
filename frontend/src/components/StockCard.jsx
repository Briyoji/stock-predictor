export default function StockCard({ ticker, price, onClick }) {
  return (
    <div className="stock-card" onClick={onClick}>
      <div className="ticker">{ticker}</div>
      <div className="price">{ticker.includes(".NS") ? "₹" : "$"} {price.toFixed(2)}</div>
    </div>
  );
}
