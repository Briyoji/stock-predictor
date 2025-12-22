from django.db import models

class Prediction(models.Model):
    LOOKBACK_CHOICES = (
        ("short", "Short"),
        ("medium", "Medium"),
        ("long", "Long"),
    )

    ticker = models.CharField(max_length=10)
    lookback = models.CharField(max_length=10, choices=LOOKBACK_CHOICES)
    prediction_date = models.DateField()
    predicted_log_return = models.FloatField()
    predicted_price = models.FloatField(null=True, blank=True)
    model_version = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["ticker", "prediction_date"]),
        ]

    def __str__(self):
        return f"{self.ticker} | {self.lookback} | {self.prediction_date}"
