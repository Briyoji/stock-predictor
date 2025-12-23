import axios from "axios";
import { API_BASE } from "./config";

export const fetchStocks = async () => {
  console.log("Initialising Stocks");
  const res = await axios.get(`${API_BASE}/stocks/`);
  return res.data;
};
