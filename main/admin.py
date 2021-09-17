from django.contrib import admin
from .models import User, Category, Contact, Subscriber, Article, Shop, Item,\
ItemInfo, Parameter, ItemParameter, Picture, Tag, Review

class UserAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class ContactAdmin(admin.ModelAdmin):
    pass

class SubscriberAdmin(admin.ModelAdmin):
    pass

class ArticleAdmin(admin.ModelAdmin):
    pass

class ShopAdmin(admin.ModelAdmin):
    pass

class ItemAdmin(admin.ModelAdmin):
    pass

class ItemInfoAdmin(admin.ModelAdmin):
    pass

class ParameterAdmin(admin.ModelAdmin):
    pass

class ItemParameterAdmin(admin.ModelAdmin):
    pass

class PictureAdmin(admin.ModelAdmin):
    pass

class TagAdmin(admin.ModelAdmin):
    pass

class ReviewAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemInfo, ItemInfoAdmin)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(ItemParameter, ItemParameterAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Review, ReviewAdmin)