from apps.transactions.serializers import AggregationRequestSerializer


def test_valid_aggregation_request():
    data = {"row_fields": "transaction_type", "column_fields": "year,status"}
    serializer = AggregationRequestSerializer(data=data)

    assert serializer.is_valid()
    assert serializer.validated_data["row_fields"] == "transaction_type"
    assert serializer.validated_data["column_fields"] == ["year", "status"]


def test_invalid_field_validation():
    data = {"row_fields": "invalid", "column_fields": "year"}
    serializer = AggregationRequestSerializer(data=data)

    assert not serializer.is_valid()
    assert "row_fields" in serializer.errors
