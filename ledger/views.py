from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import date
import json
from .models import Transaction, Category, Budget


def dashboard(request):
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    transactions = Transaction.objects.filter(date__year=year, date__month=month)
    total_income = transactions.filter(type='income').aggregate(s=Sum('amount'))['s'] or 0
    total_expense = transactions.filter(type='expense').aggregate(s=Sum('amount'))['s'] or 0
    balance = total_income - total_expense

    # Category breakdown
    expense_by_cat = (
        transactions.filter(type='expense')
        .values('category__name', 'category__color', 'category__icon')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    # Budget info
    budgets = Budget.objects.filter(year=year, month=month)
    budget_data = []
    for b in budgets:
        spent = transactions.filter(type='expense', category=b.category).aggregate(s=Sum('amount'))['s'] or 0
        budget_data.append({
            'category': b.category.name if b.category else '전체',
            'icon': b.category.icon if b.category else '💰',
            'budget': b.amount,
            'spent': spent,
            'percent': min(round(spent / b.amount * 100), 100) if b.amount else 0,
            'over': spent > b.amount,
        })

    recent = transactions[:10]

    context = {
        'year': year,
        'month': month,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'expense_by_cat': list(expense_by_cat),
        'budget_data': budget_data,
        'recent': recent,
        'categories': Category.objects.all(),
        'months': range(1, 13),
        'years': range(today.year - 2, today.year + 2),
    }
    return render(request, 'ledger/dashboard.html', context)


def transaction_list(request):
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    type_filter = request.GET.get('type', '')
    cat_filter = request.GET.get('category', '')

    qs = Transaction.objects.filter(date__year=year, date__month=month)
    if type_filter:
        qs = qs.filter(type=type_filter)
    if cat_filter:
        qs = qs.filter(category_id=cat_filter)

    context = {
        'transactions': qs,
        'categories': Category.objects.all(),
        'year': year, 'month': month,
        'type_filter': type_filter,
        'cat_filter': cat_filter,
        'months': range(1, 13),
        'years': range(today.year - 2, today.year + 2),
    }
    return render(request, 'ledger/transaction_list.html', context)


def transaction_add(request):
    if request.method == 'POST':
        t = Transaction(
            type=request.POST['type'],
            amount=int(request.POST['amount'].replace(',', '')),
            category_id=request.POST.get('category') or None,
            description=request.POST.get('description', ''),
            date=request.POST['date'],
        )
        t.save()
        return redirect('dashboard')
    categories = Category.objects.all()
    return render(request, 'ledger/transaction_form.html', {'categories': categories, 'today': date.today()})


def transaction_delete(request, pk):
    t = get_object_or_404(Transaction, pk=pk)
    t.delete()
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


def budget_list(request):
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    budgets = Budget.objects.filter(year=year, month=month)
    context = {
        'budgets': budgets,
        'categories': Category.objects.filter(type='expense'),
        'year': year, 'month': month,
        'months': range(1, 13),
        'years': range(today.year - 2, today.year + 2),
    }
    return render(request, 'ledger/budget.html', context)


def budget_save(request):
    if request.method == 'POST':
        cat_id = request.POST.get('category') or None
        year = int(request.POST['year'])
        month = int(request.POST['month'])
        amount = int(request.POST['amount'].replace(',', ''))
        Budget.objects.update_or_create(
            category_id=cat_id, year=year, month=month,
            defaults={'amount': amount}
        )
    return redirect('budget')


def stats_api(request):
    today = date.today()
    year = int(request.GET.get('year', today.year))

    monthly = []
    for m in range(1, 13):
        qs = Transaction.objects.filter(date__year=year, date__month=m)
        inc = qs.filter(type='income').aggregate(s=Sum('amount'))['s'] or 0
        exp = qs.filter(type='expense').aggregate(s=Sum('amount'))['s'] or 0
        monthly.append({'month': m, 'income': inc, 'expense': exp})

    return JsonResponse({'monthly': monthly})
