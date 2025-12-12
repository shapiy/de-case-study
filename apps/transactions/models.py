from django.db import models


class TransactionType(models.TextChoices):
    INVOICE = "invoice", "Invoice"
    BILL = "bill", "Bill"
    DIRECT_EXPENSE = "direct_expense", "Direct Expense"


class TransactionStatus(models.TextChoices):
    PAID = "paid", "Paid"
    UNPAID = "unpaid", "Unpaid"
    PARTIALLY_PAID = "partially_paid", "Partially Paid"


class Transaction(models.Model):
    transaction_type = models.CharField(
        max_length=50, choices=TransactionType.choices, db_index=True
    )
    transaction_number = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=TransactionStatus.choices, db_index=True)
    year = models.IntegerField(db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "transactions"
        ordering = ["-year", "transaction_type"]
        indexes = [
            models.Index(fields=["year", "transaction_type"]),
            models.Index(fields=["year", "status"]),
            models.Index(fields=["transaction_type", "status"]),
        ]

    def __str__(self) -> str:
        return f"{self.transaction_type} #{self.transaction_number} - ${self.amount}"
