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
        category = Category.objects.get(slug=kwargs['category_slug'])
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
    model = Item
    template_name = 'items.html'
    context_object_name = 'items_list'

    def get_queryset(self):
        category = self.kwargs['pk']
        items = Item.objects.filter(category__pk=category)
        return items