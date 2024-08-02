import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Product, Profile, Order
from django.db.models import Q, Count, F, Case, When, Value


# Create queries within functions
def get_profiles(search_string=None):
    if search_string is None:
        return ""

    profile = Profile.objects.filter(
        Q(full_name__icontains=search_string) |
        Q(email__icontains=search_string) |
        Q(phone_number__icontains=search_string)
    ).order_by('full_name')

    if not profile.exists():
        return ""

    result = []

    for p in profile:
        result.append(
            f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.orders.count()}")

    return "\n".join(result)


def get_loyal_profiles():
    profiles = Profile.objects.get_regular_customers()

    if not profiles.exists():
        return ""

    result = []

    for profile in profiles:
        result.append(f"Profile: {profile.full_name}, orders: {profile.orders.count()}")

    return "\n".join(result)


def get_last_sold_products():
    last_order = Order.objects.prefetch_related('products').last()

    if last_order is None or not last_order.prducts.exists():
        return ""

    products = ', '.join([p.name for p in last_order.products.order_by('name')])

    return f"Last sold products: {products}"


def get_top_products():
    top_products = Product.objects.annotate(orders_count=Count('order').filter(orders_count__gt=0)
                                            ).order_by('-orders_count', 'name')[:5]

    if not top_products.exists():
        return ""

    products = '\n'.join([f"{p.name}, sold {p.orders_count} times" for p in top_products])

    return f"Top products:\n" + products


def apply_discounts():
    updated_orders = Order.objects.annotate(products_count=Count('products')).filter(products_count__gt=2, is_completed=False
                                                                                     ).update(total_price=F('total_price') * 0.90)

    return f"Discount applied to {updated_orders} orders."


def complete_order():
    order = Order.objects.filter(is_completed=False).order_by('creation_date').first()

    if not order:
        return ""

    for product in order.products.all():
        product.in_stock -= 1

        if product.in_stock == 0:
            product.is_available = False

        product.save()

    Product.objects.filter(order=order).update(
        in_stock=F('in_stock') - 1,
        is_available=Case(
            When(in_stock=1, then=Value(False)),
            default=F('is_available')
        )
    )

    order.is_completed = True
    order.save()

    return "Order has been completed!"
