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
    total_cost = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='Сумма заказа')
    total_qty = models.PositiveIntegerField(default=0, verbose_name='Общее кол-во товара')

    def save(self, *args, **kwargs):
        """
        Пересчитывает общую стоимость всех позиции в Order и сохраняет.
        :param args:
        :param kwargs:
        :return:
        """
        cart_data = self.ordered_items.aggregate(sum=models.Sum('position_cost'), qty=models.Sum('quantity'))
        if cart_data.get('sum'):
            self.total_cost = cart_data.get('sum')
        else:self.total_cost = 0
        if cart_data.get('qty'):
            self.total_qty = cart_data.get('qty')
        else:self.total_qty = 0
        super().save(*args, **kwargs)

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
    position_cost = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='Стоимость позиции')

    def save(self, *args, **kwargs):
        """
        Пересчитывает цену по позиции в корзине и сохраняет объект этой позиции.
        :param args:
        :param kwargs:
        :return:
        """
        self.position_cost = self.content_object.price * self.quantity
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Заказанная позиция'
        verbose_name_plural = "Заказанные позиции"