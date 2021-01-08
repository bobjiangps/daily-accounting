from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *


def index(request):
    all_accounts = Account.objects.all()
    # categories = Category.objects.all()
    # sub_categories = SubCategory.objects.all()
    currencies = Currency.objects.all()
    ie_types = Category.CATEGORY_TYPES
    context = {
        'accounts': all_accounts,
        # 'categories': categories,
        # 'sub_categories': sub_categories,
        'currencies': currencies,
        'ie_types': ie_types
               }
    return render(request, 'accounting/index.html', context)


def retrieve_category(request):
    ie_type = request.POST.get('ie_type')
    categories = Category.objects.filter(category_type=ie_type)
    # return HttpResponse(f'{"categories": {categories}}', content_type='application/json')
    return JsonResponse(f'{"categories": {categories}}')
