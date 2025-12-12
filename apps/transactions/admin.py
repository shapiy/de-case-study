from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["transaction_number", "transaction_type", "amount", "status", "year", "created_at"]
    list_filter = ["transaction_type", "status", "year"]
    search_fields = ["transaction_number"]
    ordering = ["-year", "-created_at"]
