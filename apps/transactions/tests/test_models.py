from decimal import Decimal

import pytest

from apps.transactions.models import Transaction, TransactionType, TransactionStatus


@pytest.mark.django_db
def test_create_transaction_with_valid_data():
    transaction = Transaction.objects.create(
        transaction_type=TransactionType.INVOICE,
        transaction_number="INV-001",
        amount=Decimal("100.50"),
        status=TransactionStatus.PAID,
        year=2024,
    )
    assert transaction.transaction_type == TransactionType.INVOICE
    assert transaction.amount == Decimal("100.50")
    assert transaction.year == 2024


@pytest.mark.django_db
def test_transaction_string_representation():
    transaction = Transaction.objects.create(
        transaction_type=TransactionType.INVOICE,
        transaction_number="INV-001",
        amount=Decimal("100.50"),
        status=TransactionStatus.PAID,
        year=2024,
    )
    assert str(transaction) == "invoice #INV-001 - $100.50"


@pytest.mark.django_db
def test_negative_amount():
    transaction = Transaction.objects.create(
        transaction_type=TransactionType.BILL,
        transaction_number="REFUND-001",
        amount=Decimal("-50.00"),
        status=TransactionStatus.PAID,
        year=2024,
    )
    assert transaction.amount == Decimal("-50.00")