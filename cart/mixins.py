from django.shortcuts import HttpResponseRedirect
from django.views.generic.detail import SingleObjectMixin

from main.models import Customer, User
from cart.models import Order

class CartMixin(SingleObjectMixin):
    """
    Чтобы не повторять в каждом view код выбора корзины.
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer, is_created = Customer.objects.get_or_create(user=request.user)
            cart, is_created = Order.objects.get_or_create(customer=customer, status='cart')
        else:
            user = User.objects.get(is_anonym=True)
            customer, is_created = Customer.objects.get_or_create(user=user)
            cart, is_created = Order.objects.get_or_create(status='for_anonymous', customer=customer)

        self.cart=cart
        return super().dispatch(request, *args, **kwargs)


