from django.shortcuts import redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'wagtailadmin/login.html'

    def form_valid(self, form):
        user = form.get_user()
        if user.groups.filter(name='Visitante').exists():
            auth_login(self.request, form.get_user())
            return redirect('/')  # Redirige a la página de inicio
        return super().form_valid(form)