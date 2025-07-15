from django.urls import path
from .views import ServiceListView, ServiceDetailView,CategoryListView,CategoryDetailView

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'),
    path('<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),

]