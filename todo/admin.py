from django.contrib import admin
from .models import User_info,Order_info,product_inventry_info,raw_inventry_info


@admin.register(User_info,Order_info,product_inventry_info,raw_inventry_info)
class PersonAdmin(admin.ModelAdmin):
    pass