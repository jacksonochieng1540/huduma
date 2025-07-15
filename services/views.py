from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Service,ServiceCategory

class ServiceListView(ListView):
    model = Service
    template_name = 'list.html'
    context_object_name = 'services'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Service.objects.filter(
                Q(name__icontains=query) | 
                Q(department__icontains=query)
            )
        return Service.objects.all()

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/detail.html'
    
class CategoryListView(ListView):
    model = ServiceCategory
    template_name = 'services/category_list.html'

class CategoryDetailView(DetailView):
    model = ServiceCategory
    template_name = 'services/category_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.filter(
            category=self.object, 
            is_available=True
        )
        return context