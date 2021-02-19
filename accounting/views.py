from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from .models import *
from .forms import HistoryRecordForm, TransferRecordForm
import datetime, calendar
import decimal


def index(request):
    today = datetime.date.today()
    all_accounts = Account.objects.all()
    currencies = Currency.objects.all()
    ie_types = Category.CATEGORY_TYPES
    history_records = HistoryRecord.objects.filter(time_of_occurrence__year=today.year, time_of_occurrence__month=today.month).order_by("-time_of_occurrence")
    transfer_records = TransferRecord.objects.filter(time_of_occurrence__year=today.year, time_of_occurrence__month=today.month).order_by("-time_of_occurrence")
    income = 0
    expense = 0
    day_has_record = []
    current_month_records = {}
    day_income_expense = {}
    for hr in history_records:
        if hr.category.category_type.lower() == "expense":
            expense -= hr.amount
        elif hr.category.category_type.lower() == "income":
            income += hr.amount
        day_occur = hr.time_of_occurrence.strftime("%Y-%m-%d %A")
        if day_occur not in day_has_record:
            day_has_record.append(day_occur)
            current_month_records[day_occur] = [hr]
            day_income_expense[day_occur] = {"income": 0, "expense": 0}
            if hr.category.category_type.lower() == "expense":
                day_income_expense[day_occur]["expense"] += hr.amount
            elif hr.category.category_type.lower() == "income":
                day_income_expense[day_occur]["income"] += hr.amount
        else:
            current_month_records[day_occur].append(hr)
            if hr.category.category_type.lower() == "expense":
                day_income_expense[day_occur]["expense"] += hr.amount
            elif hr.category.category_type.lower() == "income":
                day_income_expense[day_occur]["income"] += hr.amount
    for tr in transfer_records:
        day_occur = tr.time_of_occurrence.strftime("%Y-%m-%d %A")
        if day_occur not in day_has_record:
            day_has_record.append(day_occur)
            current_month_records[day_occur] = [tr]
            day_income_expense[day_occur] = {"income": 0, "expense": 0}
        else:
            current_month_records[day_occur].append(tr)
    day_has_record.sort(reverse=True)
    context = {
        'accounts': all_accounts,
        'currencies': currencies,
        'ie_types': ie_types,
        'day_has_record': day_has_record,
        'history_records': history_records,
        'transfer_records': transfer_records,
        'current_month_income': income,
        'current_month_expense': expense,
        'surplus': income + expense,
        'current_month_records': current_month_records,
        'day_income_expense': day_income_expense
               }
    return render(request, 'accounting/index.html', context)


def retrieve_category(request):
    if request.user.is_authenticated:
        ie_type = request.POST.get('ie_type')
        categories = Category.objects.filter(category_type=ie_type)
        category_list = []
        for c in categories:
            category_list.append((c.id, c.name))
        # return HttpResponse(f'{"categories": {categories}}', content_type='application/json')
        return JsonResponse({"categories": category_list})
    else:
        return JsonResponse({"error": "unauthenticated"})


def retrieve_subcategory(request):
    if request.user.is_authenticated:
        category_type = request.POST.get('category_type')
        current_category = Category.objects.filter(name=category_type)[0]
        subcategories = SubCategory.objects.filter(parent=current_category)
        subcategory_list = []
        for sc in subcategories:
            subcategory_list.append((sc.id, sc.name))
        return JsonResponse({"subcategories": subcategory_list})
    else:
        return JsonResponse({"error": "unauthenticated"})


def record_income_expense(request):
    if request.user.is_authenticated:
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
    else:
        return JsonResponse({"error": "unauthenticated"})


def retrieve_current_month_income_expense(request):
    if request.user.is_authenticated:
        post_year = request.POST.get('year')
        post_month = request.POST.get('month')
        if post_year and post_month:
            year = int(post_year)
            month = int(post_month)
        else:
            today = datetime.date.today()
            year = today.year
            month = today.month
        month_has_days = calendar.monthrange(year, month)[1]
        days = [datetime.date(year, month, day).strftime("%Y-%m-%d") for day in range(1, month_has_days+1)]
        days_income = []
        days_expense = []
        category_names = []
        month_category_income = {}
        month_category_expense = {}
        month_total_income = 0
        month_total_expense = 0
        month_history_records = HistoryRecord.objects.filter(time_of_occurrence__year=year, time_of_occurrence__month=month).order_by("time_of_occurrence")
        for day in days:
            day_history_records = month_history_records.filter(time_of_occurrence__day=int(day.split("-")[-1]))
            day_income = 0
            day_expense = 0
            for hr in day_history_records:
                hr_category = hr.category
                if hr_category.category_type.lower() == "expense":
                    day_expense += hr.amount
                    month_total_expense += hr.amount
                    if hr_category.name not in category_names:
                        category_names.append(hr_category.name)
                        month_category_expense[hr_category.name] = {"value": hr.amount, "name": hr_category.name}
                    else:
                        month_category_expense[hr_category.name]["value"] += hr.amount
                elif hr_category.category_type.lower() == "income":
                    day_income += hr.amount
                    month_total_income += hr.amount
                    if hr_category.name not in category_names:
                        category_names.append(hr_category.name)
                        month_category_income[hr_category.name] = {"value": hr.amount, "name": hr_category.name}
                    else:
                        month_category_income[hr_category.name]["value"] += hr.amount
            days_income.append(day_income)
            days_expense.append(day_expense)
        return JsonResponse({"days": days,
                             "days_income": days_income,
                             "days_expense": days_expense,
                             "month_total_income": month_total_income,
                             "month_total_expense": month_total_expense,
                             "month_category_names": category_names,
                             "month_category_income": list(month_category_income.values()),
                             "month_category_expense": list(month_category_expense.values())})
    else:
        return JsonResponse({"error": "unauthenticated"})


def retrieve_current_year_income_expense(request):
    if request.user.is_authenticated:
        post_year = request.POST.get('year')
        if post_year:
            year = int(post_year)
        else:
            today = datetime.date.today()
            year = today.year
        months = [i for i in range(1, 13)]
        months_income = []
        months_expense = []
        category_names = []
        year_category_income = {}
        year_category_expense = {}
        year_total_income = 0
        year_total_expense = 0
        year_history_records = HistoryRecord.objects.filter(time_of_occurrence__year=year).order_by("time_of_occurrence")
        for month in months:
            month_history_records = year_history_records.filter(time_of_occurrence__month=month)
            month_income = 0
            month_expense = 0
            for hr in month_history_records:
                hr_category = hr.category
                if hr_category.category_type.lower() == "expense":
                    month_expense += hr.amount
                    year_total_expense += hr.amount
                    if hr_category.name not in category_names:
                        category_names.append(hr_category.name)
                        year_category_expense[hr_category.name] = {"value": hr.amount, "name": hr_category.name}
                    else:
                        year_category_expense[hr_category.name]["value"] += hr.amount
                elif hr_category.category_type.lower() == "income":
                    month_income += hr.amount
                    year_total_income += hr.amount
                    if hr_category.name not in category_names:
                        category_names.append(hr_category.name)
                        year_category_income[hr_category.name] = {"value": hr.amount, "name": hr_category.name}
                    else:
                        year_category_income[hr_category.name]["value"] += hr.amount
            months_income.append(month_income)
            months_expense.append(month_expense)
        return JsonResponse({"months": months,
                             "months_income": months_income,
                             "months_expense": months_expense,
                             "year_total_income": year_total_income,
                             "year_total_expense": year_total_expense,
                             "year_category_names": category_names,
                             "year_category_income": list(year_category_income.values()),
                             "year_category_expense": list(year_category_expense.values())})
    else:
        return JsonResponse({"error": "unauthenticated"})


def retrieve_year_has_data(request):
    if request.user.is_authenticated:
        hr_first = HistoryRecord.objects.order_by("time_of_occurrence").first()
        hr_last = HistoryRecord.objects.order_by("time_of_occurrence").last()
        year_list = [y for y in range(hr_last.time_of_occurrence.year, hr_first.time_of_occurrence.year-1, -1)]
        return JsonResponse({"years": year_list})
    else:
        return JsonResponse({"error": "unauthenticated"})


def retrieve_month_has_data(request):
    if request.user.is_authenticated:
        year = request.POST.get('year')
        hr = HistoryRecord.objects.filter(time_of_occurrence__year=year).order_by("time_of_occurrence")
        hr_first = hr.first()
        hr_last = hr.last()
        month_list = [m for m in range(hr_last.time_of_occurrence.month, hr_first.time_of_occurrence.month-1, -1)]
        return JsonResponse({"months": month_list})
    else:
        return JsonResponse({"error": "unauthenticated"})


def search_record(request):
    if request.user.is_authenticated:
        keyword = request.POST.get('keyword')
        categories = Category.objects.filter(name__icontains=keyword)
        subcategories = SubCategory.objects.filter(name__icontains=keyword)
        hrs = HistoryRecord.objects.filter(Q(category__in=categories) | Q(sub_category__in=subcategories) | Q(comment__icontains=keyword) | Q(amount__icontains=keyword))
        records = []
        for hr in hrs:
            day_occur = hr.time_of_occurrence.strftime("%Y-%m-%d %A")
            if hr.sub_category:
                sub_category = hr.sub_category.name
            else:
                sub_category = "no sub category"
            if hr.comment:
                comment = hr.comment
            else:
                comment = ""
            records.append({
                "day": day_occur,
                "category": hr.category.name,
                "subcategory": sub_category,
                "amount": hr.amount,
                "comment": comment,
                "account": hr.account.name,
                "ie_type": hr.category.category_type.lower()
            })
        return JsonResponse({"records": records})
    else:
        return JsonResponse({"error": "unauthenticated"})


def filter_record_by_date(request):
    if request.user.is_authenticated:
        post_year = request.POST.get('year')
        post_month = request.POST.get('month')
        history_records = HistoryRecord.objects.filter(time_of_occurrence__year=post_year, time_of_occurrence__month=post_month).order_by("-time_of_occurrence")
        transfer_records = TransferRecord.objects.filter(time_of_occurrence__year=post_year, time_of_occurrence__month=post_month).order_by("-time_of_occurrence")
        day_has_record = []
        custom_month_records = {}
        for hr in history_records:
            day_occur = hr.time_of_occurrence.strftime("%Y-%m-%d %A")
            if hr.sub_category:
                sub_category = hr.sub_category.name
            else:
                sub_category = "no sub category"
            if hr.comment:
                comment = hr.comment
            else:
                comment = ""
            new_hr = {
                "category": hr.category.name,
                "subcategory": sub_category,
                "amount": hr.amount,
                "comment": comment,
                "account": hr.account.name,
                "ie_type": hr.category.category_type.lower(),
                "record_type": "income_expense"
            }
            if day_occur not in day_has_record:
                day_has_record.append(day_occur)
                custom_month_records[day_occur] = [new_hr]
            else:
                custom_month_records[day_occur].append(new_hr)
        for tr in transfer_records:
            day_occur = tr.time_of_occurrence.strftime("%Y-%m-%d %A")
            if tr.comment:
                comment = tr.comment
            else:
                comment = ""
            new_tr = {
                "amount": tr.amount,
                "comment": comment,
                "from_account": tr.from_account.name,
                "to_account": tr.to_account.name,
                "record_type": "transfer"
            }
            if day_occur not in day_has_record:
                day_has_record.append(day_occur)
                custom_month_records[day_occur] = [new_tr]
            else:
                custom_month_records[day_occur].append(new_tr)
        return JsonResponse({'day_has_record': day_has_record, "records": custom_month_records})
    else:
        return JsonResponse({"error": "unauthenticated"})


def transfer_between_accounts(request):
    if request.user.is_authenticated:
        time_now = timezone.now()
        form = TransferRecordForm(request.POST)
        if form.is_valid():
            from_account = form.cleaned_data['from_account']
            to_account = form.cleaned_data['to_account']
            if from_account != to_account:
                transfer_amount = form.cleaned_data['amount']
                transfer_comment = form.cleaned_data['comment']
                time_occur = form.cleaned_data['time_of_occurrence']
                transfer_record = TransferRecord(from_account=from_account,
                                                 to_account=to_account,
                                                 amount=transfer_amount,
                                                 comment=transfer_comment,
                                                 time_of_occurrence=time_occur,
                                                 created_date=time_now,
                                                 updated_date=time_now
                                                 )
                transfer_record.save()
                from_account.amount -= decimal.Decimal(transfer_amount)
                from_account.save()
                to_account.amount += decimal.Decimal(transfer_amount)
                to_account.save()
            else:
                print("WARNING: You are transferring money amount between the same account!")
        return redirect(index)
    else:
        return JsonResponse({"error": "unauthenticated"})
