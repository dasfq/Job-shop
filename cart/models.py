from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from main.models import *




class DeliveryAdress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Покупатель', related_name='delivery_adress')
    adress = models.CharField(verbose_name='Адрес', blank=True, max_length=150)
    default = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Адрес доставки"
        verbose_name_plural = "Адреса доставки"


class DeliveryPhone(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Покупатель', related_name='delivery_phone')
    phone_number = models.CharField(verbose_name='Телефон', blank=True, max_length=12, unique=True)
    default = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Телефон получаетля"
        verbose_name_plural = "Телефоны получателя"


class DeliveryContact(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Покупатель', related_name='delivery_contact')
    full_name = models.CharField(verbose_name='Ф.И.О.', max_length=30, blank=True)
    default = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Ф.И.О. получателя"
        verbose_name_plural = "Ф.И.О. получателя"

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Order(models.Model):

    class StatusChoices(models.TextChoices):
        CART = 'cart', 'Корзина'
        NEW = 'new', 'Ожидает подтверждения'
        CONFIRMED = 'confirmed', "Подтверждён"
        PAYMENT = 'pay', "Ожидает оплаты"
        ASSEMBLED = 'assembled', "Собран"
        SENT = 'sent', "Отправлен"
        DELIVERED = 'delivered', "Доставлен"
        CANCELED = 'canceled', "Отменён"
        FOR_ANONYMOUS = 'anonymous', "Аноним"

    customer = models.ForeignKey(Customer, verbose_name='Покупатель', related_name='orders', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        verbose_name='Статус',
        choices=StatusChoices.choices,
        max_length=10,
        default=StatusChoices.CART)
    total_cost = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='Сумма заказа')
    total_qty = models.PositiveIntegerField(default=0, verbose_name='Общее кол-во товара')
    delivery_date = models.DateField(blank=True, null=True, verbose_name='Дата доставки')
    delivery_contact = models.CharField(max_length=30, default='', blank=True, null=True, verbose_name='Ф.И.О. получателя')
    delivery_adress = models.CharField(max_length=50, default='', blank=True, null=True, verbose_name='Адресс доставки')
    delivery_phone = models.CharField(max_length=11, default='', blank=True, null=True, verbose_name='Телефон получателя')

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

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'Order {self.customer} {self.status}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = "Заказы"
        ordering = ('-date',)


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
        price = self.content_object.discount_price
        if not price:
            price = self.content_object.price
        self.position_cost = price * int(self.quantity)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Заказанная позиция'
        verbose_name_plural = "Заказанные позиции"


