from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from .forms import HistoryRecordForm
import datetime
import decimal


def index(request):
    today = datetime.date.today()
    all_accounts = Account.objects.all()
    currencies = Currency.objects.all()
    ie_types = Category.CATEGORY_TYPES
    history_records = HistoryRecord.objects.filter(time_of_occurrence__year=today.year, time_of_occurrence__month=today.month).order_by("-time_of_occurrence")
    income = 0
    expense = 0
    for hr in history_records:
        if hr.category.category_type.lower() == "expense":
            expense -= hr.amount
        elif hr.category.category_type.lower() == "income":
            income += hr.amount
    context = {
        'accounts': all_accounts,
        'currencies': currencies,
        'ie_types': ie_types,
        'history_records': history_records,
        'current_month_income': income,
        'current_month_expense': expense
               }
    return render(request, 'accounting/index.html', context)


def retrieve_category(request):
    ie_type = request.POST.get('ie_type')
    categories = Category.objects.filter(category_type=ie_type)
    category_list = []
    for c in categories:
        category_list.append((c.id, c.name))
    # return HttpResponse(f'{"categories": {categories}}', content_type='application/json')
    return JsonResponse({"categories": category_list})


def retrieve_subcategory(request):
    category_type = request.POST.get('category_type')
    current_category = Category.objects.filter(name=category_type)[0]
    subcategories = SubCategory.objects.filter(parent=current_category)
    subcategory_list = []
    for sc in subcategories:
        subcategory_list.append((sc.id, sc.name))
    return JsonResponse({"subcategories": subcategory_list})


def record_income_expense(request):
    sub_category = request.POST.get('sub_category')
    time_now = timezone.now()
    if sub_category == "select value":
        try:
            account = request.POST.get('account')
            category = request.POST.get('category')
            currency = request.POST.get('currency')
            amount = request.POST.get('amount')
            comment = request.POST.get('comment')
            time_occur = request.POST.get('time_of_occurrence')
            history_record = HistoryRecord(account_id=account,
                                           category_id=category,
                                           currency_id=currency,
                                           amount=amount,
                                           comment=comment,
                                           time_of_occurrence=time_occur,
                                           created_date=time_now,
                                           updated_date=time_now
                                           )
            history_record.save()
            current_account = Account.objects.filter(id=account)[0]
            current_ie_type = Category.objects.filter(id=category)[0].category_type
            if current_ie_type.lower() == "expense":
                current_account.amount -= decimal.Decimal(amount)
            elif current_ie_type.lower() == "income":
                current_account.amount += decimal.Decimal(amount)
            current_account.save()
        except Exception as e:
            print("not valid in request with error: %s" % str(e))
    else:
        form = HistoryRecordForm(request.POST)
        if form.is_valid():
            account = form.cleaned_data['account']
            category = form.cleaned_data['category']
            sub_category = form.cleaned_data['sub_category']
            currency = form.cleaned_data['currency']
            amount = form.cleaned_data['amount']
            comment = form.cleaned_data['comment']
            time_occur = form.cleaned_data['time_of_occurrence']
            history_record = HistoryRecord(account=account,
                                           category=category,
                                           sub_category=sub_category,
                                           currency=currency,
                                           amount=amount,
                                           comment=comment,
                                           time_of_occurrence=time_occur,
                                           created_date=time_now,
                                           updated_date=time_now
                                           )
            history_record.save()
            current_ie_type = category.category_type
            if current_ie_type.lower() == "expense":
                account.amount -= decimal.Decimal(amount)
            elif current_ie_type.lower() == "income":
                account.amount += decimal.Decimal(amount)
            account.save()
        else:
            print("not valid in form")
    return redirect(index)
