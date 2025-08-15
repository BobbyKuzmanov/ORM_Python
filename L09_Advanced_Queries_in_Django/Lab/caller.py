import os
from decimal import Decimal

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Product, Order
from django.db.models import Sum


def product_quantity_ordered():
    result = []
    orders = (
        Product.objects.annotate(
            total=Sum('orderproduct__quantity'))
        .values('name', 'total')
        .order_by('-total')
    )

    for order in orders:
        result.append(f"Quantity ordered of {order['name']}: {order['total']}")

    return "\n".join(result)


def ordered_products_per_customer():
    orders = Order.objects.prefetch_related('orderproduct_set__product__category').order_by('id')

    result = []
    for order in orders:
        result.append(f"Order ID: {order.id}, Customer: {order.customer.username}")

        for order_product in order.orderproduct_set.all():
            result.append(f"- Product: {order_product.product.name}, Category: {order_product.product.category.name}")


    return "\n".join(result)


def filter_products():
    # Fetch all available products with prices greater than 3.00 BGN
    products = Product.objects.filter(is_available=True, price__gt=3.00).order_by('-price', 'name')

    # Format the result
    result = []
    for product in products:
        result.append(f"{product.name}: {product.price}lv.")

    return "\n".join(result)


def give_discount():
    # Fetch all available products with prices greater than 3.00 BGN
    products = Product.objects.filter(is_available=True, price__gt=3.00)

    # Apply a 30% discount to each product
    for product in products:
        product.price *= Decimal(0.70)
        product.save()

    # Fetch all available products again to get the updated prices
    updated_products = Product.objects.filter(is_available=True).order_by('-price', 'name')

    # Format the result
    result = []
    for product in updated_products:
        result.append(f"{product.name}: {product.price}lv.")

    return "\n".join(result)


