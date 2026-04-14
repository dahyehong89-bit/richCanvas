from django.contrib import admin
from .models import Transaction, Category, Budget

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['icon', 'name', 'type', 'color']
    list_filter = ['type']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['date', 'type', 'category', 'description', 'amount']
    list_filter = ['type', 'date', 'category']
    date_hierarchy = 'date'

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['year', 'month', 'category', 'amount']
