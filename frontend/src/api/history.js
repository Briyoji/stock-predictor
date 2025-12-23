import axios from "axios";
import { API_BASE } from "./config";

export const fetchHistory = async (ticker, range) => {
  const res = await axios.get(
    `${API_BASE}/stocks/${ticker}/history/?range=${range}`
    // `${API_BASE}/stocks/AAPL/history/?range=1mo`
  );
  console.log("Hist Data", res.data)
  return res.data.prices;
};
