from rest_framework import serializers

class PredictionRequestSerializer(serializers.Serializer):
    ticker = serializers.CharField(max_length=25)
    lookback = serializers.ChoiceField(choices=["short", "medium", "long"])
