from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('retrieve_category/', views.retrieve_category, name='retrieve_category'),
    path('retrieve_subcategory/', views.retrieve_subcategory, name='retrieve_subcategory'),
    path('record_income_expense/', views.record_income_expense, name='record_income_expense'),
    path('retrieve_current_month_income_expense/', views.retrieve_current_month_income_expense, name='retrieve_current_month_income_expense'),
    path('retrieve_current_year_income_expense/', views.retrieve_current_year_income_expense, name='retrieve_current_year_income_expense'),
    path('retrieve_year_has_data/', views.retrieve_year_has_data, name='retrieve_year_has_data'),
    path('retrieve_month_has_data/', views.retrieve_month_has_data, name='retrieve_month_has_data'),
    path('search_record/', views.search_record, name='search_record'),
    path('filter_record_by_date/', views.filter_record_by_date, name='filter_record_by_date'),
    path('transfer-between-accounts/', views.transfer_between_accounts, name='transfer_between_accounts')
]
