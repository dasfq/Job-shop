from django.shortcuts import render
from django.views.generic import ListView, DetailView, View

from main.models import Category, Item

class IndexView(ListView):
    template_name = 'main/index.html'
    context_object_name = 'items_list'

    def get_queryset(self):
        qt = []
        for cls in Item.__subclasses__():
            newest = cls.objects.order_by('-id')[:5]
            qt.extend(newest)
        return qt


class ItemDetail(DetailView):
    context_object_name = 'item'
    template_name = 'main/item_detail.html'
    slug_url_kwarg = 'item_slug'
    slug_field = 'slug'

    def dispatch(self, request, *args, **kwargs):
        item_name = kwargs['item_model_name'].capitalize()
        category = Category.objects.get(item_model_name=item_name)
        for cls in Item.__subclasses__():
            if cls.objects.filter(category=category):
                self.model = cls
                return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        param_list = self.object.get_parameters_list()
        context['parameters'] = param_list
        return context


class ItemList(ListView):
    template_name = 'main/items_list.html'
    context_object_name = 'items_list'

    def dispatch(self, request, *args, **kwargs):
        model_name = self.kwargs['item_model_name'].capitalize()
        for model in Item.__subclasses__():
            if model.objects.filter(category__item_model_name=model_name):
                self.model = model
                return super().dispatch(request, *args, **kwargs)