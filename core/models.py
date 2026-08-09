from django.db import models

# Create your models here.
class Products(models.Model):
    CATEGORY_CHOICES = [
        ('alcohol', 'Alcohol'),
        ('non_alcohol', 'Non_alcohol'),
        ('coffee', 'Coffee'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.PositiveIntegerField()
    stock_quantity = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Tables(models.Model):
    number = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f"Table {self.number}"

class Order(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    ]

    table = models.ForeignKey(Tables,on_delete=models.PROTECT,related_name="orders")
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="open")

    def __str__(self):
        return f"Order {self.id} - Table {self.table.number}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey(Products,on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.PositiveIntegerField()

    @property
    def subtotal(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"