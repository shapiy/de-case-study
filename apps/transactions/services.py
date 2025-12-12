from collections import defaultdict
from decimal import Decimal
from typing import Any

from django.db.models import QuerySet, Sum

from .models import Transaction


class TransactionAggregator:
    ALLOWED_FIELDS = ["transaction_type", "status", "year"]

    @classmethod
    def aggregate(
        cls, row_field: str, column_fields: list[str], queryset: QuerySet | None = None
    ) -> dict[str, Any]:
        if queryset is None:
            queryset = Transaction.objects.all()

        group_by = [row_field] + column_fields

        aggregated = queryset.values(*group_by).annotate(total=Sum("amount")).order_by(*group_by)

        data = cls._build_nested_structure(aggregated, row_field, column_fields)
        totals = cls._calculate_totals(aggregated, row_field, column_fields)

        return {
            "row_field": row_field,
            "column_fields": column_fields,
            "data": data,
            "totals": totals,
        }

    @classmethod
    def _build_nested_structure(
        cls, aggregated: QuerySet, row_field: str, column_fields: list[str]
    ) -> dict[str, Any]:
        result: dict[str, Any] = defaultdict(lambda: defaultdict(Decimal))

        for row in aggregated:
            row_value = row[row_field]
            total = row["total"] or Decimal("0")

            col_key = cls._make_column_key(row, column_fields)
            result[str(row_value)][col_key] = float(total)

        return dict(result)

    @classmethod
    def _calculate_totals(
        cls, aggregated: QuerySet, row_field: str, column_fields: list[str]
    ) -> dict[str, Any]:
        column_totals: dict[str, Decimal] = defaultdict(Decimal)
        row_totals: dict[str, Decimal] = defaultdict(Decimal)
        grand_total = Decimal("0")

        for row in aggregated:
            row_value = str(row[row_field])
            col_key = cls._make_column_key(row, column_fields)
            total = row["total"] or Decimal("0")

            column_totals[col_key] += total
            row_totals[row_value] += total
            grand_total += total

        return {
            "by_column": {k: float(v) for k, v in column_totals.items()},
            "by_row": {k: float(v) for k, v in row_totals.items()},
            "grand_total": float(grand_total),
        }

    @classmethod
    def _make_column_key(cls, row: dict[str, Any], column_fields: list[str]) -> str:
        parts = [str(row[field]) for field in column_fields]
        return " | ".join(parts)
