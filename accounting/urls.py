from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('retrieve_category/', views.retrieve_category, name='retrieve_category'),
    path('retrieve_subcategory/', views.retrieve_subcategory, name='retrieve_subcategory'),
]
