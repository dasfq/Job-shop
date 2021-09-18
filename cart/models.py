# from django.db import models
# from main.models import User
#
#
# class Order(models.Model):
#
#     class StatusChoices(models.TextChoices):
#         cart = 'cart', 'корзина'
#         NEW = 'new', 'новый'
#         CONFIRMED = 'confirmed', "подтверждён"
#         ASSEMBLED = 'assembled', "собран"
#         SENT = 'sent', "отправлен"
#         DELIVERED = 'delivered', "доставлен"
#         CANCELED = 'canceled', "отменён"
#
#     user = models.ForeignKey(User, verbose_name='Пользователь', related_name='orders', blank=True,
#                              on_delete=models.CASCADE)
#     date = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(
#         verbose_name='Статус',
#         choices=StatusChoices.choices,
#         max_length=10,
#         default=StatusChoices.cart)
#
#     class Meta:
#         verbose_name = 'Заказ'
#         verbose_name_plural = "Заказы"
#         ordering = ('-date',)
#
#     def __str__(self):
#         return str(self.date)
#
#
# class OrderInfo(models.Model):
#     order = models.ForeignKey(Order, verbose_name='Заказ', related_name='ordered_items', blank=True,
#                               on_delete=models.CASCADE)
#     item_info = models.ForeignKey(ItemInfo, verbose_name='Информация о продукте', related_name='ordered_items', blank=True,
#                              on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(verbose_name='Количество')
#
#     class Meta:
#         verbose_name = 'Заказанная позиция'
#         verbose_name_plural = "Заказанные позиции"