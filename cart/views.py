from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import CreateView, View, DetailView, ListView

from cart.models import *
from main.models import *
from cart.forms import OrderFormSet, OrderForm


class AddToCart(View):

    def get(self, request, *args, **kwargs):
        """
        Добавляет OrderInfo в Order. При этом изменяет количество и сохраняет объект.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
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
        cart.save()
        return HttpResponseRedirect(redirect_to=request.GET.get('next'))



class CartDetail(View):
    template_name = 'cart/cart.html'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name, context={})


class CartChange(View):

    def post(self, request, *args, **kwargs):
        qty = request.POST.get('qty')
        item_slug = kwargs['item_slug']
        model_name = kwargs['model_name']
        ct = ContentType.objects.get(app_label='main', model=model_name)
        item = ct.get_object_for_this_type(slug=item_slug)
        customer = Customer.objects.get(user=request.user)
        cart, is_created = Order.objects.get_or_create(customer=customer, status='cart')
        position = OrderInfo.objects.get(order=cart, content_type=ct, object_id=item.id)
        position.quantity = qty
        position.save()
        cart.save()
        return HttpResponseRedirect(reverse('cart'))


class CartDeleteItem(View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        cart, is_created = Order.objects.get_or_create(customer=customer, status='cart')
        position = OrderInfo.objects.get(id=kwargs['id'], order=cart)
        position.delete()
        cart.save()
        return HttpResponseRedirect(reverse('cart'))

class OrderCreate(View):
    model = Order
    form_class = OrderFormSet
    context_object_name = 'order'

    def get(self, request, *args, **kwargs):
        print(12312312312312312312)
        customer = Customer.objects.get(user=request.user)
        cart, is_created = Order.objects.get_or_create(customer=customer, status='cart')
        cart.status = 'new'
        cart.save()
        return HttpResponseRedirect(reverse('order_detail', kwargs={'pk': cart.id}))

class OrderDetail(DetailView):
    model = Order
    template_name = 'cart/order.html'
    # form_class = OrderForm
    context_object_name = 'order'


class OrderList(ListView):
    model = Order
    template_name = 'cart/orders_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        customer = Customer.objects.get(user=self.request.user)
        return Order.objects.filter(customer=customer).exclude(status='cart')



