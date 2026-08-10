from django.contrib import admin
from .models import Tables, Products, Order, OrderItem


@admin.register(Tables)
class TablesAdmin(admin.ModelAdmin):
    list_display = ("number",)


admin.site.register(Products)
admin.site.register(Order)
admin.site.register(OrderItem)