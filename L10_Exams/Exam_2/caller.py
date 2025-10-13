import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.db.models import F, Q, Count

from main_app.models import Profile, Product, Order


# Create queries within functions
def get_loyal_profiles():
    loyal_profiles = Profile.objects.annotate(num_of_orders=Count('profile_orders')).filter(
        num_of_orders__gt=2).order_by('-num_of_orders')

    if not loyal_profiles:
        return ""

    return "\n".join([
        f"Profile: {profile.full_name}, orders: {profile.num_of_orders}"
        for profile in loyal_profiles
    ])


def get_last_sold_products():
    last_order = Order.objects.order_by('-creation_date').first()

    if not last_order:
        return ""

    products = last_order.products.order_by('name')
    product_names = ', '.join([product.name for product in products])

    return f"Last sold products: {product_names}"


def get_profiles(search_string=None):
    queryset = Profile.objects.annotate(num_of_orders=Count('profile_orders'))

    if search_string:
        queryset = queryset.filter(
            Q(full_name__icontains=search_string) |
            Q(email__icontains=search_string) |
            Q(phone_number__icontains=search_string)
        )

    queryset = queryset.order_by('full_name')

    if not queryset:
        return ""

    return "\n".join([
        f"Profile: {profile.full_name}, email: {profile.email}, phone number: {profile.phone_number}, orders: {profile.num_of_orders}"
        for profile in queryset
    ])


def get_top_products():
    top_products = Product.objects.annotate(
        num_orders=Count('products_order')
    ).order_by('-num_orders', 'name')[:5]

    if not top_products:
        return ""

    return "Top products:" + "\n" + "\n".join([
        f"{product.name}, sold {product.num_orders} times"
        for product in top_products
    ])


def apply_discounts():
    orders_to_update = Order.objects.filter(
        is_completed=False,
        products__gt=2
    ).distinct()

    updated_count = orders_to_update.update(
        total_price=F('total_price') * 0.9
    )

    return f"Discount applied to {updated_count} orders."


def complete_order():
    order_to_complete = Order.objects.filter(is_completed=False).order_by('creation_date').first()

    if not order_to_complete:
        return ""

    for product in order_to_complete.products.all():
        product.in_stock -= 1
        if product.in_stock == 0:
            product.is_available = False
        product.save()

    order_to_complete.is_completed = True
    order_to_complete.save()

    return "Order has been completed!"