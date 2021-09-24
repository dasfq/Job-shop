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
    customer = Customer.objects.get(user=request.user)
    try:
        cart = Order.objects.get(customer=customer, status='cart')
    except:
        cart = None
    return {'cart': cart}