from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from .models import User
from .forms import UserRegistrationForm
from django.shortcuts import redirect

class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True



class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return redirect('login')  


class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'core/register.html'
    success_url = '/login/'