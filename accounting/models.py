from django.db import models
from django.utils import timezone


class Currency(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Account(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, default=1)
    icon = models.CharField(max_length=100, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Category(models.Model):
    CATEGORY_TYPES = (
       ("Income", "income"),
       ("Expense", "expense")
    )
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)
    category_type = models.CharField(choices=CATEGORY_TYPES, default=CATEGORY_TYPES[0][1], max_length=100)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)
    parent = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class HistoryRecord(models.Model):
    time_of_occurrence = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, default=1)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    comment = models.CharField(max_length=500)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
