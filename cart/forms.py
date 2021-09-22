from django import forms
from django.forms import inlineformset_factory

from cart.models import *

OrderFormSet = inlineformset_factory(Order, OrderInfo, fields=('quantity',))

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('customer', 'status', 'delivery_date',)