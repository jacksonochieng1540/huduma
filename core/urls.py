from django.urls import path
from core.views import  CustomLoginView,CustomLogoutView,RegisterView
urlpatterns = [
    path('login/',CustomLoginView.as_view(),name='CustomLoginView'),
    path('logout/',CustomLogoutView.as_view(),name='CustomLogoutView'),
]
