import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

// Styles
import "./styles/global.css";
import "./styles/stocks.css";
import "./styles/modal.css";
import "./styles/chart.css";
import "./styles/predict.css";


ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
