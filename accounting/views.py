from django.shortcuts import render
from .models import *


def index(request):
    all_accounts = Account.objects.all()
    categories = Category.objects.all()
    sub_categories = SubCategory.objects.all()
    currencies = Currency.objects.all()
    ie_types = []
    for t in Category.CATEGORY_TYPES:
        ie_types.append(t[0])
    context = {
        'accounts': all_accounts,
        'categories': categories,
        'sub_categories': sub_categories,
        'currencies': currencies,
        'ie_types': ie_types
               }
    return render(request, 'accounting/index.html', context)
