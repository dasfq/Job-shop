from django.shortcuts import render, HttpResponseRedirect, reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, View

from cart.models import *
from main.models import *
from cart.forms import OrderFormSet, OrderForm


class AddToCart(View):
    form_class = OrderForm

    def get(self, request, *args, **kwargs):
        item_model_name = kwargs['item_model_name']
        item_slug = kwargs['item_slug']
        customer = Customer.objects.get(user=request.user)
        cart, is_created = Order.objects.get_or_create(customer=customer, status='cart')
        ct = ContentType.objects.get(app_label='main', model=item_model_name)
        item = ct.get_object_for_this_type(slug=item_slug)
        cart_item, is_created = OrderInfo.objects.get_or_create(content_type=ct, object_id = item.id, order=cart)
        if not is_created:
            cart_item.quantity += 1
            cart_item.save()
        return HttpResponseRedirect(redirect_to=request.GET.get('next'))



class CartDetail(View):
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



