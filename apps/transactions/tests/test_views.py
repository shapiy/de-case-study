from decimal import Decimal

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.transactions.models import Transaction, TransactionType, TransactionStatus


@pytest.mark.django_db
def test_list_all_transactions():
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
        status=TransactionStatus.PAID,
        year=2025,
    )

    client = APIClient()
    url = reverse("transaction-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 2


@pytest.mark.django_db
def test_filter_by_transaction_type():
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
        status=TransactionStatus.PAID,
        year=2024,
    )

    client = APIClient()
    url = reverse("transaction-list")
    response = client.get(url, {"transaction_type": "invoice"})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1


@pytest.mark.django_db
def test_filter_by_year():
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
        status=TransactionStatus.PAID,
        year=2025,
    )

    client = APIClient()
    url = reverse("transaction-list")
    response = client.get(url, {"year": "2024"})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1


@pytest.mark.django_db
def test_aggregate_endpoint_success():
    Transaction.objects.create(
        transaction_type=TransactionType.INVOICE,
        transaction_number="INV-001",
        amount=Decimal("100.00"),
        status=TransactionStatus.PAID,
        year=2024,
    )

    client = APIClient()
    url = reverse("transaction-aggregate")
    response = client.get(url, {"row_fields": "transaction_type", "column_fields": "year"})

    assert response.status_code == status.HTTP_200_OK
    assert "row_field" in response.data
    assert "column_fields" in response.data
    assert "data" in response.data
    assert "totals" in response.data


@pytest.mark.django_db
def test_aggregate_with_multiple_column_fields_api():
    Transaction.objects.create(
        transaction_type=TransactionType.INVOICE,
        transaction_number="INV-001",
        amount=Decimal("100.00"),
        status=TransactionStatus.PAID,
        year=2024,
    )

    client = APIClient()
    url = reverse("transaction-aggregate")
    response = client.get(url, {"row_fields": "year", "column_fields": "transaction_type,status"})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["column_fields"] == ["transaction_type", "status"]


@pytest.mark.django_db
def test_aggregate_missing_required_fields():
    client = APIClient()
    url = reverse("transaction-aggregate")
    response = client.get(url, {"column_fields": "year"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_aggregate_invalid_field():
    client = APIClient()
    url = reverse("transaction-aggregate")
    response = client.get(url, {"row_fields": "invalid_field", "column_fields": "year"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
