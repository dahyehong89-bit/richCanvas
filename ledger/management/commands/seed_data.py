from django.core.management.base import BaseCommand
from ledger.models import Category, Transaction, Budget
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = '샘플 데이터 생성'

    def handle(self, *args, **kwargs):
        cats = [
            ('식비', 'expense', '🍚', '#f87171'),
            ('카페', 'expense', '☕', '#fb923c'),
            ('교통', 'expense', '🚌', '#fbbf24'),
            ('쇼핑', 'expense', '🛍️', '#a78bfa'),
            ('의료', 'expense', '💊', '#60a5fa'),
            ('문화', 'expense', '🎬', '#f472b6'),
            ('월급', 'income', '💵', '#34d399'),
            ('부업', 'income', '💻', '#6ee7b7'),
        ]
        cat_objs = {}
        for name, typ, icon, color in cats:
            c, _ = Category.objects.get_or_create(name=name, type=typ, defaults={'icon': icon, 'color': color})
            cat_objs[name] = c

        today = date.today()
        expense_cats = [cat_objs[n] for n in ['식비','카페','교통','쇼핑','의료','문화']]
        for i in range(60):
            d = today - timedelta(days=i)
            Transaction.objects.create(
                type='expense', amount=random.choice([3000,5000,8000,12000,15000,25000,35000]),
                category=random.choice(expense_cats),
                description=random.choice(['스타벅스','점심식사','버스','마트','영화','병원','편의점']),
                date=d
            )
        for m in range(3):
            mo = today.month - m
            yr = today.year
            if mo <= 0:
                mo += 12; yr -= 1
            Transaction.objects.create(type='income', amount=3000000, category=cat_objs['월급'], description='월급', date=date(yr, mo, 25))

        for name, amt in [('식비', 400000), ('카페', 100000), ('쇼핑', 200000)]:
            Budget.objects.get_or_create(category=cat_objs[name], year=today.year, month=today.month, defaults={'amount': amt})

        self.stdout.write(self.style.SUCCESS('샘플 데이터 생성 완료!'))
