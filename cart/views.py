from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View, ListView, UpdateView, DetailView
from django.db import transaction

from cart.models import *
from main.models import *
from cart.forms import OrderForm
from cart.mixins import CartMixin


class AddToCart(CartMixin, View):

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
        ct = ContentType.objects.get(app_label='main', model=item_model_name)
        item = ct.get_object_for_this_type(slug=item_slug)
        cart_item, is_created = OrderInfo.objects.get_or_create(content_type=ct, object_id = item.id, order=self.cart)
        if not is_created:
            cart_item.quantity += 1
            cart_item.save()
        self.cart.save()
        return HttpResponseRedirect(redirect_to=request.GET.get('next'))



class CartDetail(CartMixin, View):
    template_name = 'cart/cart.html'

    def get(self, request, *args, **kwargs):
        context = {
            'cart': self.cart
        }
        return render(request, template_name=self.template_name, context=context)


class CartChange(CartMixin, View):

    def post(self, request, *args, **kwargs):
        qty = request.POST.get('qty')
        item_slug = kwargs['item_slug']
        model_name = kwargs['model_name']
        ct = ContentType.objects.get(app_label='main', model=model_name)
        item = ct.get_object_for_this_type(slug=item_slug)
        position = OrderInfo.objects.get(order=self.cart, content_type=ct, object_id=item.id)
        position.quantity = qty
        position.save()
        self.cart.save()
        return HttpResponseRedirect(reverse('cart'))


class CartDeleteItem(CartMixin, View):

    def get(self, request, *args, **kwargs):
        position = OrderInfo.objects.get(id=kwargs['id'], order=self.cart)
        position.delete()
        self.cart.save()
        return HttpResponseRedirect(reverse('cart'))


class OrderList(ListView):
    model = Order
    template_name = 'cart/orders_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        customer = Customer.objects.get(user=self.request.user)
        return Order.objects.filter(customer=customer).exclude(status='cart')


class OrderEdit(CartMixin, View):
    template_name = 'cart/order_edit.html'
    model = Order

    def get(self, request, *args, **kwargs):
        self.object = self.cart
        context = self.get_context_data(**kwargs)
        return render(request, template_name=self.template_name, context=context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_form = OrderForm(instance=self.object)
        context['order'] = self.cart
        context['form'] = order_form
        return context


class OrderCheckout(CartMixin, UpdateView):
    model = Order
    context_object_name = 'order'
    form_class = OrderForm
    template_name = 'cart/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.object
        return context

    @transaction.atomic
    def form_valid(self, form):
        self.object.status = 'new'
        super().form_valid(form)
        return HttpResponseRedirect(reverse('order_detail', kwargs={'pk': self.object.pk}))

    def form_invalid(self, form):
        return render(self.request, 'cart/order_edit.html', context=self.get_context_data())


class OrderDetail(CartMixin, DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'cart/order_detail.html'
