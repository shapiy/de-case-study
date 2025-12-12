from decimal import Decimal
from typing import Any, Dict, List

from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "transaction_type",
            "transaction_number",
            "amount",
            "status",
            "year",
        ]


class AggregationRequestSerializer(serializers.Serializer):
    row_fields = serializers.CharField(required=True, help_text="Field to group rows by (e.g., 'transaction_type')")
    column_fields = serializers.CharField(required=True, help_text="Comma-separated fields for columns (e.g., 'year,status')")

    def validate_row_fields(self, value: str) -> str:
        allowed = ["transaction_type", "status", "year"]
        if value not in allowed:
            raise serializers.ValidationError(f"Must be one of: {', '.join(allowed)}")
        return value

    def validate_column_fields(self, value: str) -> List[str]:
        allowed = ["transaction_type", "status", "year"]
        fields = [f.strip() for f in value.split(",")]

        for field in fields:
            if field not in allowed:
                raise serializers.ValidationError(f"All fields must be one of: {', '.join(allowed)}")

        return fields


class AggregationResponseSerializer(serializers.Serializer):
    row_field = serializers.CharField()
    column_fields = serializers.ListField(child=serializers.CharField())
    data = serializers.DictField()
    totals = serializers.DictField()