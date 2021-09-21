from .models import Category, Item

def categories(request):
    """
    Формирует список категорий и количество товара в них для вывода в Каталоге.
    main_{item_model.__name__}_items - это relative field в m2m между Category и Item.
    :param request:
    :return:
    """
    cat_list = []
    qt = Category.objects.all()
    for item_class in Item.__subclasses__():
        cat = qt.get(slug=f'{item_class.__name__.lower()}' + 's')
        cat.items_number = len(item_class.objects.all())
        cat_list.append(cat)
    return {"categories": cat_list}