from django.views.generic import View
from main.models import Customer
from cart.models import Order

class CartMixin(View):
    """
    Чтобы не повторять в каждом view код выбора корзины.
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer, is_created = Customer.objects.get_or_create(user=request.user)
            cart, is_created = Order.objects.get_or_create(customer=customer, status='cart')
        else:
            cart, is_created = Order.objects.get_or_create(status='for_anonymous')
        self.cart=cart
        return super().dispatch(request, *args, **kwargs)


