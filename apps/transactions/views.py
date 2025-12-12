from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from .models import Transaction
from .serializers import (
    AggregationRequestSerializer,
    AggregationResponseSerializer,
    TransactionSerializer,
)
from .services import TransactionAggregator


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["transaction_type", "status", "year"]
    ordering_fields = ["year", "transaction_type", "amount", "created_at"]
    ordering = ["-year", "transaction_type"]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="row_fields",
                description="Field to group rows by (transaction_type, status, or year)",
                required=True,
                type=str,
            ),
            OpenApiParameter(
                name="column_fields",
                description="Comma-separated fields for columns (e.g., 'year,status')",
                required=True,
                type=str,
            ),
        ],
        responses={200: AggregationResponseSerializer},
    )
    @action(detail=False, methods=["get"], url_path="aggregate")
    def aggregate(self, request):
        request_serializer = AggregationRequestSerializer(data=request.query_params)
        request_serializer.is_valid(raise_exception=True)

        row_field = request_serializer.validated_data["row_fields"]
        column_fields = request_serializer.validated_data["column_fields"]

        result = TransactionAggregator.aggregate(row_field, column_fields)

        response_serializer = AggregationResponseSerializer(result)
        return Response(response_serializer.data)
