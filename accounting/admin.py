from django.contrib import admin
from .models import *

admin.site.register(Currency)
admin.site.register(Account)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(HistoryRecord)
