from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime

from .serializers import PredictionRequestSerializer
from .services.market_data import get_stock_list
from .services.market_data import get_historical_prices

from .models import Prediction
from .serializers import PredictionRequestSerializer
from .services.fetch_data import fetch_lookback_data
# from .services.feature_builder import build_features
from ml.data.feature_engineer import build_features
from ml.data.target_builder import add_log_return_target
from ml import FEATURE_COLS
from .services.inference import run_inference


class StockListView(APIView):
    def get(self, request):
        data = get_stock_list()
        return Response(data, status=status.HTTP_200_OK)
    


class StockHistoryView(APIView):
    def get(self, request, ticker):
        range_key = request.GET.get("range", "1y")

        try:
            prices = get_historical_prices(ticker.upper(), range_key)
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "ticker": ticker.upper(),
                "range": range_key,
                "prices": prices,
            },
            status=status.HTTP_200_OK,
        )




class PredictView(APIView):
    def post(self, request):
        serializer = PredictionRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ticker = serializer.validated_data["ticker"].upper()
        lookback = serializer.validated_data["lookback"]

        try:
            df = fetch_lookback_data(ticker, lookback)
            df = add_log_return_target(df)
            features = build_features(df)[FEATURE_COLS]
            features = features.to_numpy(dtype="float32")

            log_return, model_version = run_inference(features, lookback)

            last_close = float(df["Close"].iloc[-1])
            predicted_price = round(last_close * (2.71828 ** log_return), 2)

            prediction = Prediction.objects.create(
                ticker=ticker,
                lookback=lookback,
                prediction_date=datetime.today(),
                predicted_log_return=log_return,
                predicted_price=predicted_price,
                model_version=model_version,
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "ticker": ticker,
                "lookback": lookback,
                "predicted_log_return": round(log_return, 6),
                "predicted_price": predicted_price,
                "model_version": model_version,
            },
            status=status.HTTP_200_OK,
        )