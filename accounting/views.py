from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
from .forms import HistoryRecordForm


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
    category_list = []
    for c in categories:
        category_list.append(c.name)
    # return HttpResponse(f'{"categories": {categories}}', content_type='application/json')
    return JsonResponse({"categories": category_list})


def retrieve_subcategory(request):
    category_type = request.POST.get('category_type')
    current_category = Category.objects.filter(name=category_type)[0]
    subcategories = SubCategory.objects.filter(parent=current_category)
    subcategory_list = []
    for sc in subcategories:
        subcategory_list.append(sc.name)
    return JsonResponse({"subcategories": subcategory_list})


def record_income_expense(request):
    # form = HistoryRecordForm(request.POST)
    # print(form)
    print(request.POST)
