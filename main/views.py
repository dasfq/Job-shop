from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView

from main.models import Category, Item

def index(request):
    template_name = 'index.html'
    context = {
        'user': request.user
    }
    return render(request, template_name, context)


class CategoryDetail(DetailView):
    model = Category
    context_object_name = 'category_detail'
    template_name = 'items.html'

class ItemList(ListView):
    model = Item
    template_name = 'items.html'
    context_object_name = 'items_list'

    def get_queryset(self):
        category = self.kwargs['pk']
        items = Item.objects.filter(category__pk=category)
        return items