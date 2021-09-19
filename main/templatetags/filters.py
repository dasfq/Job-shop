from django import template
import math

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