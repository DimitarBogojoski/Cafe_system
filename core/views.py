from django.shortcuts import render
from .models import Products, Tables


def table_list(request):
    tables = Tables.objects.all().order_by("number")
    products = Products.objects.filter(
        is_available=True
    ).order_by("category", "name")

    for table in tables:
        table.is_occupied = table.orders.filter(
            status="open"
        ).exists()

    return render(
        request,
        "table_list.html",
        {
            "tables": tables,
            "products": products,
        }
    )