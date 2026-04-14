from django.db import models
from django.utils import timezone


class Category(models.Model):
    TYPE_CHOICES = [('income', '수입'), ('expense', '지출')]
    name = models.CharField(max_length=50, verbose_name='카테고리명')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name='유형')
    icon = models.CharField(max_length=10, default='💰', verbose_name='아이콘')
    color = models.CharField(max_length=7, default='#6366f1', verbose_name='색상')

    class Meta:
        verbose_name = '카테고리'
        verbose_name_plural = '카테고리 목록'

    def __str__(self):
        return f"{self.icon} {self.name}"


class Transaction(models.Model):
    TYPE_CHOICES = [('income', '수입'), ('expense', '지출')]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name='유형')
    amount = models.PositiveIntegerField(verbose_name='금액')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='카테고리')
    description = models.CharField(max_length=200, blank=True, verbose_name='내용')
    date = models.DateField(default=timezone.now, verbose_name='날짜')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '거래내역'
        verbose_name_plural = '거래내역 목록'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"[{self.get_type_display()}] {self.description} {self.amount:,}원"


class Budget(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, verbose_name='카테고리')
    amount = models.PositiveIntegerField(verbose_name='예산금액')
    year = models.IntegerField(verbose_name='연도')
    month = models.IntegerField(verbose_name='월')

    class Meta:
        verbose_name = '예산'
        verbose_name_plural = '예산 목록'
        unique_together = ['category', 'year', 'month']

    def __str__(self):
        cat = self.category.name if self.category else '전체'
        return f"{self.year}년 {self.month}월 {cat} 예산: {self.amount:,}원"
