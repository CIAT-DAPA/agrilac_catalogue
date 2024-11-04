from django.shortcuts import redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import CustomUser  # Importa tu modelo de usuario personalizado
from .forms import CustomUserCreationForm, CustomAuthenticationForm  # Importa tus formularios personalizados
from activity_logs.utils import log_user_activity  # Importa tu función para registrar actividad
from django.utils import timezone


# Vista personalizada de Login
class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'  # Usa la plantilla personalizada

    def form_valid(self, form):
        user = form.get_user()
        # Registrar el inicio de sesión en los logs de actividad
        log_user_activity(
            user=user,
            action="Inicio de sesión",
            request=self.request,
            extra_data={}
        )

        if user.role == 'visitor':
            auth_login(self.request, form.get_user())
            return redirect('/')  # Redirige a la página principal para visitantes
        return super().form_valid(form)
    
    def form_invalid(self, form):
        # Si el formulario es inválido, regresa con los errores
        return self.render_to_response(self.get_context_data(form=form))

# Nueva vista para el registro de usuarios
class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'  # Plantilla para el formulario de registro
    success_url = reverse_lazy('wagtailadmin_login')  # Redirige al login tras el registro exitoso
