from django.core.exceptions import ValidationError
from django.db import transaction

from core.models import Order,OrderItem,Products

@transaction.atomic
def add_product_to_order(order_id,product_id,quantity):
    order = Order.objects.get(id=order_id, status="open")
    product=Products.objects.select_for_update().get(id=product_id)

    if not product.is_available:
        raise ValidationError("Product is not available")

    if product.stock_quantity < quantity:
        raise ValidationError(f"Only {product.stock_quantity} units of {product.name} remain")

    product.stock_quantity-=quantity
    product.save(update_fields=["stock_quantity"])

    item,created = OrderItem.objects.get_or_create(order=order,product=product,defaults={"quantity":quantity,"unit_price":product.price})

    if not created:
        item.quantity+=quantity
        item.save(update_fields=["quantity"])

    return item

@transaction.atomic
def remove_order_item(item_id):
    item = OrderItem.objects.select_related("product").get(id=item_id)
    product = Products.objects.select_for_update().get(id=item.product.id)
    product.stock_quantity+=item.quantity
    product.save(update_fields=["stock_quantity"])
    item.delete()

@transaction.atomic
def pay_order(order_id):
    order = Order.objects.select_for_update().get(id=order_id,status="open")
    order.status = "paid"
    order.save(update_fields=["status"])
    return order