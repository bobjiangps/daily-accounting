from django.db import models
from django.utils import timezone


class Currency(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Account(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, default=1)
    icon = models.CharField(max_length=100, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_date']


class Category(models.Model):
    CATEGORY_TYPES = (
        ("expense", "支出"),
        ("income", "收入"),
    )
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)
    category_type = models.CharField(choices=CATEGORY_TYPES, default=CATEGORY_TYPES[0][0], max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)
    parent = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class HistoryRecord(models.Model):
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, default=1)
    time_of_occurrence = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, default=1)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    comment = models.CharField(max_length=500, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-time_of_occurrence']


class TransferRecord(models.Model):
    from_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, default=1, related_name='from_account')
    to_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, default=2, related_name='to_account')
    time_of_occurrence = models.DateTimeField(default=timezone.now)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, default=1)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    comment = models.CharField(max_length=500, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-time_of_occurrence']
