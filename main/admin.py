from django.contrib import admin

from django.contrib.contenttypes.admin import GenericStackedInline
from django.forms import ModelMultipleChoiceField, ModelChoiceField
from cart.models import *
from main.models import *

class UserAdmin(admin.ModelAdmin):
    exclude = ('is_anonym',)

class ContactInline(admin.TabularInline):
    # model = Contact
    extra = 1


# class CustomerAdmin(admin.ModelAdmin):
    # inlines = [ContactInline,]


class ParameterInline(admin.StackedInline):
    model = Parameter.category.through
    extra = 3

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'item_model_name': ('name',)}
    inlines = [ParameterInline,]
    exclude = ('items_number',)


class ItemParameterInline(GenericStackedInline):
    """
    Класс для вставки полей дочерних классов Item в inline при добавлении нового товара.
    """
    model = ItemParameter

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Оставляет в раскрывающемся списке только параметры, которые есть у данной категории товара.
        :param db_field:
        :param request:
        :param kwargs:
        :return:
        """
        category = request.path.split('/')[3]
        if db_field.name == 'parameter':
            return ModelChoiceField(Parameter.objects.filter(category__item_model_name=category.capitalize()))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ItemPictureInline(GenericStackedInline):
    model = ItemPicture
    extra = 1

class NotebookAdmin(admin.ModelAdmin):
    """
    Ноутбуки
    """
    inlines = [ItemPictureInline, ItemParameterInline,]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Перед тем как отобразить поле на странице функция проверяет его и фильтрует его значения в раскрывающемся списке.
        :param db_field:
        :param request:
        :param kwargs:
        :return:
        """
        cat_name = request.path.split('/')[3].capitalize()
        if db_field.name == 'category':
            return ModelMultipleChoiceField(Category.objects.filter(item_model_name=cat_name))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PhoneAdmin(admin.ModelAdmin):
    """
    Смартфоны
    """
    inlines = [ItemPictureInline, ItemParameterInline,]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        cat_name = request.path.split('/')[3].capitalize()
        if db_field.name == 'category':
            return ModelMultipleChoiceField(Category.objects.filter(item_model_name=cat_name))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class FridgeAdmin(admin.ModelAdmin):
    """
    Холодильники
    """
    inlines = [ItemPictureInline, ItemParameterInline,]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        cat_name = request.path.split('/')[3].capitalize()
        if db_field.name == 'category':
            return ModelMultipleChoiceField(Category.objects.filter(item_model_name=cat_name))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# def ItemMaker(*args, **kwargs):
#     cls_list = []
#     for cls in args:
#         new_class_name = cls.__name__ + 'Admin'
#         cls_list.append(type(new_class_name, (admin.ModelAdmin,), {'inlines':[ItemParameterInline,]}))
#     print(cls_list)
#     return cls_list
#
# ItemMaker(Notebook, Phone, Fridge)


# admin.site.register(Customer, CustomerAdmin)
admin.site.register(Customer)
admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subscriber)
admin.site.register(Parameter)
admin.site.register(ItemPicture)
admin.site.register(Tag)
admin.site.register(Review)
admin.site.register(Brand)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Phone, PhoneAdmin)
admin.site.register(Fridge, FridgeAdmin)
admin.site.register(Favourite)