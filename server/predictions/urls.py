from django.urls import path
from .views import PredictView, StockListView, StockHistoryView

urlpatterns = [
    path("stocks/", StockListView.as_view(), name="stock-list"),
    path("stocks/<str:ticker>/history/", StockHistoryView.as_view(), name="stock-history"),
    path("predict/", PredictView.as_view(), name="predict"),
]
