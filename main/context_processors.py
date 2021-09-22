from .models import Category, Item

def categories(request):
    """
    Формирует список категорий.
    :param request:
    :return:
    """
    qt = Category.objects.all()
    return {"categories": qt}

    # cat_list = []
    # qt = Category.objects.all()
    # for item_class in Item.__subclasses__():
    #     cat = qt.get(slug=f'{item_class.__name__.lower()}' + 's')
    #     cat.items_number = len(item_class.objects.all())
    #     cat_list.append(cat)
