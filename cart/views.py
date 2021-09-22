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
        item_model_name = kwargs['item_model_name']
        print(item_model_name)
        item_slug = kwargs['item_slug']
        print(item_slug)
        customer = Customer.objects.get(user=request.user)
        cart, is_created = Order.objects.get_or_create(customer=customer, status='cart')
        print(cart, is_created)
        ct = ContentType.objects.get(app_label='main', model=item_model_name)
        #
        print('ct', ct)
        # i = Item.__subclasses__()[0]._meta.model_name
        # print(i)
        # item_model = [cls for cls in Item.__subclasses__() if cls._meta.model_name == item_model_name]
        # print(item_model)
        # item_model = item_model[0]
        # item = item_model.objects.get(slug=item_slug)
        item = ct.get_object_for_this_type(slug=item_slug)
        print('item', item)
        cart_item, is_created = OrderInfo.objects.get_or_create(content_type=ct, object_id = item.id, order=cart)
        if not is_created:
            cart_item.quantity += 1
            cart_item.save()
        print(cart_item, is_created)
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



