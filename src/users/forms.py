from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.contrib.auth.models import Group

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        # Añadir clases a los campos de formulario
        self.fields['username'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Usuario'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Contraseña'
        })

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')  # Agrega los campos que necesites
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # Añadir clases a los campos de formulario
        self.fields['username'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Usuario'
        })
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Nombre'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Apellidos'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Correo electrónico'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Contraseña'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Confirmar contraseña'
        })

    def save(self, commit=True):
        # Sobrescribimos el método `save` para asegurarnos de que el rol sea 'visitor' por defecto
        user = super().save(commit=False)
        user.role = CustomUser.VISITOR  # Establecemos el rol como 'visitor'
        if commit:
            user.save()  # Guarda el usuario en la base de datos para asignarle un ID

        # Luego de guardarlo, podemos asignar el grupo
        group = Group.objects.get(name='Visitante')
        user.groups.add(group)
        
        return user