from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import DetailView, ListView, CreateView, UpdateView, View

from cart.models import *
from main.models import *
from cart.forms import OrderFormSet, OrderForm


class AddToCart(UpdateView):
    model = Order
    template_name = 'cart/add_to_cart.html'
    success_url = '/cart/'
    form_class = OrderForm

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        cart, is_created = Order.objects.get_or_create(customer=customer, status='cart')
        print(cart, is_created)
        item =
        cart_item = OrderInfo.objects.
        return HttpResponseRedirect('/cart/')



class CartDetail(View):
    model = Order
    context_object_name = 'order'
    slug_url_kwarg = 'id'
    slug_field = 'id'
    template_name = 'cart/cart.html'

    def get(self, request, *args, **kwargs):
        customer, is_created = Customer.objects.get_or_create(user=request.user)
        cart, is_created = Order.objects.get_or_create(customer=customer, status="cart")
        context = {
            'cart': cart,
        }
        return render(request, template_name=self.template_name, context=context)


class OrderCreate(CreateView):
    model = Order
    success_url = '/'
    form_class = OrderFormSet
    template_name = 'cart/order_create.html'



