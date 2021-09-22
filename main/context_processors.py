from .models import Category, Item

def categories(request):
    """
    Формирует список категорий.
    :param request:
    :return:
    """
    qt = Category.objects.all()
    return {"categories": qt}