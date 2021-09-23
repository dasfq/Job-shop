from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from main.models import *


class Order(models.Model):

    class StatusChoices(models.TextChoices):
        CART = 'cart', 'корзина'
        NEW = 'new', 'новый'
        CONFIRMED = 'confirmed', "подтверждён"
        ASSEMBLED = 'assembled', "собран"
        SENT = 'sent', "отправлен"
        DELIVERED = 'delivered', "доставлен"
        CANCELED = 'canceled', "отменён"

    customer = models.ForeignKey(Customer, verbose_name='Покупатель', related_name='orders', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        verbose_name='Статус',
        choices=StatusChoices.choices,
        max_length=10,
        default=StatusChoices.CART)
    delivery_date = models.DateField(blank=True, null=True, verbose_name='Дата достаки')

    @property
    def items_count(self):
        return self.ordered_items.count()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = "Заказы"
        ordering = ('-date',)

    def __str__(self):
        return f'Order {self.customer} {self.status}'


class OrderInfo(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='ordered_items', blank=True,
                              on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=1, null=True, blank=True)

    @property
    def position_cost(self):
        return self.content_object.price * self.quantity

    class Meta:
        verbose_name = 'Заказанная позиция'
        verbose_name_plural = "Заказанные позиции"