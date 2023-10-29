from datetime import datetime, timedelta

from django.shortcuts import render
from .models import User, Order


def index(request):
    return render(request, "lesson_2/index.html")


def basket(request, user_id):
    products = []
    user = User.objects.filter(pk=user_id).first()
    orders = Order.objects.filter(customer=user).all()
    for order in orders:
        products.append(order.products.all())
    products.reverse()
    context = {'user': user, 'orders': orders, 'products': products}
    print(products)
    return render(request, "lesson_2/user_all_orders.html", context)


def sorted_basket(request, user_id, days_ago):
    product = []
    product_set = []
    now = datetime.now()
    before = now - timedelta(days=days_ago)
    user = User.objects.filter(pk=user_id).first()
    orders = Order.objects.filter(customer=user, date_ordered__range=(before, now)).all()
    for order in orders:
        products = order.products.all()
        for product in products:
            if product not in product_set:
                product_set.append(product)
    context = {'user': user, 'product_set': product_set, 'days': days_ago}
    return render(request, 'lesson_2/user_all_product.html', context)