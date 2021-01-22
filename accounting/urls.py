from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('retrieve_category/', views.retrieve_category, name='retrieve_category'),
    path('retrieve_subcategory/', views.retrieve_subcategory, name='retrieve_subcategory'),
    path('record_income_expense/', views.record_income_expense, name='record_income_expense'),
    path('retrieve_current_month_income_expense/', views.retrieve_current_month_income_expense, name='retrieve_current_month_income_expense'),
    path('retrieve_current_year_income_expense/', views.retrieve_current_year_income_expense, name='retrieve_current_year_income_expense'),
]
