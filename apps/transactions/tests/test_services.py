from decimal import Decimal

import pytest

from apps.transactions.models import Transaction, TransactionType, TransactionStatus
from apps.transactions.services import TransactionAggregator


@pytest.mark.django_db
def test_aggregate_by_transaction_type_and_year():
    Transaction.objects.create(
        transaction_type=TransactionType.INVOICE,
        transaction_number="INV-001",
        amount=Decimal("100.00"),
        status=TransactionStatus.PAID,
        year=2024,
    )
    Transaction.objects.create(
        transaction_type=TransactionType.BILL,
        transaction_number="BILL-001",
        amount=Decimal("150.00"),
        status=TransactionStatus.UNPAID,
        year=2025,
    )

    result = TransactionAggregator.aggregate("transaction_type", ["year"])

    assert result["row_field"] == "transaction_type"
    assert result["column_fields"] == ["year"]
    assert "data" in result
    assert "totals" in result


@pytest.mark.django_db
def test_aggregate_with_multiple_column_fields():
    Transaction.objects.create(
        transaction_type=TransactionType.INVOICE,
        transaction_number="INV-001",
        amount=Decimal("100.00"),
        status=TransactionStatus.PAID,
        year=2024,
    )

    result = TransactionAggregator.aggregate("year", ["transaction_type", "status"])

    assert result["row_field"] == "year"
    assert result["column_fields"] == ["transaction_type", "status"]
    assert "data" in result


@pytest.mark.django_db
def test_totals_calculation():
    Transaction.objects.create(
        transaction_type=TransactionType.INVOICE,
        transaction_number="INV-001",
        amount=Decimal("100.00"),
        status=TransactionStatus.PAID,
        year=2024,
    )
    Transaction.objects.create(
        transaction_type=TransactionType.BILL,
        transaction_number="BILL-001",
        amount=Decimal("150.00"),
        status=TransactionStatus.UNPAID,
        year=2025,
    )

    result = TransactionAggregator.aggregate("transaction_type", ["year"])
    expected_total = float(Decimal("100.00") + Decimal("150.00"))

    assert result["totals"]["grand_total"] == expected_total


@pytest.mark.django_db
def test_aggregate_with_empty_queryset():
    result = TransactionAggregator.aggregate("transaction_type", ["year"])

    assert result["data"] == {}
    assert result["totals"]["grand_total"] == 0.0