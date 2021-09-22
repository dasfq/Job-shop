from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView

from main.models import Category, Item

def index(request):
    template_name = 'index.html'
    context = {
        'user': request.user
    }
    return render(request, template_name, context)


class ItemDetail(DetailView):
    context_object_name = 'item'
    template_name = 'item_detail.html'
    slug_url_kwarg = 'item_slug'
    slug_field = 'slug'

    def dispatch(self, request, *args, **kwargs):
        category = Category.objects.get(item_model_name=kwargs['item_model_name'])
        for cls in Item.__subclasses__():
            if cls.objects.filter(category=category):
                self.model = cls
                return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        param_list = self.object.get_parameters_list()
        context['parameters'] = param_list
        return context


class CategoryDetail(DetailView):
    model = Category
    template_name = 'category_detail.html'
    slug_url_kwarg = 'category_slug'
    slug_field = 'slug'

class ItemList(ListView):
    template_name = 'category_detail.html'
    context_object_name = 'items_list'

    def dispatch(self, request, *args, **kwargs):
        self.model = self.kwargs['item_model_name']
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        items = self.model_name.objects.all()
        return items
