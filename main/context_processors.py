from .models import Category, Customer
from cart.models import Order

def categories(request):
    """
    Формирует список категорий.
    :param request:
    :return:
    """
    qt = Category.objects.all()
    return {"categories": qt}

def cart(request):
    """
    Чтобы в панели навигации на кнопке "Корзина" высчитывалось кол-во товара
    :param request:
    :return:
    """
    customer = Customer.objects.get(user=request.user)
    cart,is_created = Order.objects.get_or_create(customer=customer, status='cart')
    return {'cart': cart}