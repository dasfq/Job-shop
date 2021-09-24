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
    total_cost = models.PositiveIntegerField(default=0, verbose_name='Сумма заказа')

    @property
    def items_count(self):
        return self.ordered_items.count()

    def save(self, *args, **kwargs):
        """
        Пересчитывает общую стоимость всех позиции в Order и сохраняет.
        :param args:
        :param kwargs:
        :return:
        """
        total_cost = self.ordered_items.aggregate(sum=models.Sum('position_cost'))
        if total_cost.get('sum'):
            self.total_cost = total_cost.get('sum')
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
    position_cost = models.PositiveIntegerField(default=0)

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