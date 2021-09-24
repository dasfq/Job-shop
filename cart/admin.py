from django.contrib import admin
from cart.models import Order, OrderInfo

class OrderInfoInline(admin.StackedInline):
    model = OrderInfo
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'date', 'delivery_date', 'customer', 'total_cost')
    list_filter = ('status', 'delivery_date',)
    # search_fields = ()
    inlines = [OrderInfoInline]

class OrderInfoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderInfo, OrderInfoAdmin)
