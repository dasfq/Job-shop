from django import template
import math
from django.db.models import F

register = template.Library()

@register.filter
def currency(value, currency):
    '''
    Add currency symbol
    '''
    if currency.lower()=='rub':
        return f'₽{value}'

@register.filter
def discount(value, discount):
    '''
    Добавляет зачёркнутую цену "до скидки".
    '''
    price = float(value)/(1-discount/100)
    return int(math.ceil(price/100))*100

@register.filter
def status(value):
    choices = {
    'new': 'Новый',
    'confirmed': "Подтверждён",
    'assembled': "Собран",
    'sent': "Отправлен",
    'delivered': "Доставлен",
    'canceled': "Отменён",
    }
    return choices[value]