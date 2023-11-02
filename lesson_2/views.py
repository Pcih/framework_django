import logging

from datetime import datetime, timedelta
from django.shortcuts import redirect
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .models import User, Order, Product
from .forms import ProductFormWidget, ProductChoiceForm


logger = logging.getLogger(__name__)



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


def product_update_form(request, product_id):

    if request.method == 'POST':
        form = ProductFormWidget(request.POST, request.FILES)
        if form.is_valid():
            # Делаем что-то с данными
            logger.info(f'Получили {form.cleaned_data=}.')
            name = form.cleaned_data.get('name')
            price = form.cleaned_data.get('price')
            description = form.cleaned_data.get('description')
            number = form.cleaned_data.get('number')

            image = request.FILES['image']
            fs = FileSystemStorage()
            fs.save(image.name, image)



            product = Product.objects.filter(pk=product_id).first()
            product.name = name
            product.price = price
            product.description = description
            product.quantity = number
            product.image = image.name

            product.save()

    else:
        form = ProductFormWidget()
    return render(request, 'lesson_2/product_update.html', {'form': form})

def product_update_id_form(request):
    if request.method == 'POST':
        form = ProductChoiceForm(request.POST)
        if form.is_valid():
            logger.info(f'Получили {form.cleaned_data=}.')
            prod_id = form.cleaned_data.get('product_id') # получил id продукта - номер из выпадающего списка
            response = redirect(f'/lesson_2/product_update/{prod_id}')
            return response
    else:
        form = ProductChoiceForm()
    return render(request, 'lesson_2/product_update_id.html', {'form': form})


def index(request):
    return render(request, "lesson_2/index.html")