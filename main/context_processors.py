from .models import Category, Customer, User
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
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        cart, is_created = Order.objects.get_or_create(customer=customer, status='cart')
    else:
        user = User.objects.get(is_anonym=True)
        customer, is_created = Customer.objects.get_or_create(user=user)
        cart, is_created = Order.objects.get_or_create(status='for_anonymous', customer=customer)
    return {'cart': cart}