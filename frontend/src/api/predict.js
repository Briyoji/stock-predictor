import axios from "axios";
import { API_BASE } from "./config";

export const predictNextDay = async (ticker, lookback) => {
  const res = await axios.post(`${API_BASE}/predict/`, {
    ticker,
    lookback,
  });
  return res.data;
};
