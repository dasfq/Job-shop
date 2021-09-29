from django import forms
from django.core.exceptions import ValidationError

from cart.models import *



class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delivery_date'].label = 'Дата доставки'

    def clean_delivery_date(self):
        date = self.cleaned_data['delivery_date']
        if not date:
            raise ValidationError('Введите дату доставки')
        return date

    def clean_delivery_adress(self):
        adress = self.cleaned_data['delivery_adress']
        if not adress:
            raise ValidationError('Введите адрес доставки')
        return adress

    def clean_delivery_contact(self):
        contact = self.cleaned_data['delivery_contact']
        if not contact:
            raise ValidationError('Укажите контактное лицо')
        return contact

    def clean_delivery_phone(self):
        phone = self.cleaned_data['delivery_phone']
        if not phone:
            raise ValidationError('Укажите номер телефона')
        return phone

    class Meta:
        model = Order
        fields=('delivery_date', 'delivery_contact', 'delivery_adress', 'delivery_phone', )
        extra=0
        can_delete=False
        widgets={
        'delivery_date': forms.TextInput(attrs={'type': 'date'})
    }