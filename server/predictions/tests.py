from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework import status

class StockListAPITest(APITestCase):
    def test_stock_list_success(self):
        response = self.client.get("/api/stocks/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreater(len(response.data), 0)

        stock = response.data[0]

        self.assertIn("ticker", stock)
        self.assertIn("name", stock)
        self.assertIn("last_close", stock)
        self.assertIn("last_updated", stock)

        self.assertIsInstance(stock["last_close"], (int, float))



class StockHistoryAPITest(APITestCase):
    def test_stock_history_valid_range(self):
        response = self.client.get(
            "/api/stocks/AAPL/history/?range=1y"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["ticker"], "AAPL")
        self.assertEqual(data["range"], "1y")
        self.assertIn("prices", data)

        prices = data["prices"]
        self.assertGreater(len(prices), 0)

        row = prices[0]
        self.assertIn("date", row)
        self.assertIn("close", row)

    def test_stock_history_invalid_range(self):
        response = self.client.get(
            "/api/stocks/AAPL/history/?range=10y"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)


from predictions.models import Prediction

class PredictAPITest(APITestCase):
    def test_predict_success(self):
        payload = {
            "ticker": "AAPL",
            "lookback": "short",
        }

        response = self.client.post(
            "/api/predict/",
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data

        self.assertEqual(data["ticker"], "AAPL")
        self.assertEqual(data["lookback"], "short")
        self.assertIn("predicted_log_return", data)
        self.assertIn("predicted_price", data)
        self.assertIn("model_version", data)

        self.assertIsInstance(data["predicted_log_return"], float)
        self.assertIsInstance(data["predicted_price"], (int, float))

        # Ensure DB persistence
        self.assertEqual(Prediction.objects.count(), 1)

    def test_predict_invalid_lookback(self):
        payload = {
            "ticker": "AAPL",
            "lookback": "ultra",
        }

        response = self.client.post(
            "/api/predict/",
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
