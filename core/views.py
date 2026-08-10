import json
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Products, Tables,Order
from .services.order_service import *


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

def order_detail(request, table_id):
    order = Order.objects.filter(
        table_id=table_id,
        status="open"
    ).first()

    if order is None:
        return JsonResponse({"items": [], "total": 0})

    items = [
        {
            "id": item.id,
            "product_name": item.product.name,
            "quantity": item.quantity,
            "unit_price": item.unit_price,
            "subtotal": item.subtotal,
        }
        for item in order.items.all()
    ]

    return JsonResponse({
        "order_id": order.id,
        "items": items,
        "total": order.total,
    })


@require_POST
def order_add_item(request, table_id):
    data = json.loads(request.body)
    product_id = data.get("product_id")
    quantity = int(data.get("quantity", 1))

    order = get_or_create_open_order(table_id)

    try:
        add_product_to_order(order.id, product_id, quantity)
    except ValidationError as e:
        return JsonResponse({"error": str(e)}, status=400)

    return order_detail(request, table_id)


@require_POST
def order_remove_item(request, item_id):
    item = OrderItem.objects.get(id=item_id)
    table_id = item.order.table_id

    remove_order_item(item_id)

    return order_detail(request, table_id)


@require_POST
def order_pay(request, table_id):
    order = Order.objects.filter(
        table_id=table_id,
        status="open"
    ).first()

    if order is None:
        return JsonResponse({"error": "No open order for this table."}, status=400)

    pay_order(order.id)

    return JsonResponse({"status": "paid"})