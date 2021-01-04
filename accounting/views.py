from django.shortcuts import render
from .models import *


def index(request):
    all_accounts = Account.objects.all()
    sub_categories = SubCategory.objects.all()
    context = {
        'accounts': all_accounts,
        'sub_categories': sub_categories
               }
    return render(request, 'accounting/index.html', context)
