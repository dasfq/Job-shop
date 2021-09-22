from django.contrib import admin
from cart.models import Order, OrderInfo

class OrderAdmin(admin.ModelAdmin):
    pass

class OrderInfoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderInfo, OrderInfoAdmin)
