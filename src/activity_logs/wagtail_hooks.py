from django.urls import path, reverse
from wagtail.admin.menu import MenuItem
from wagtail import hooks
from django.utils.translation import gettext_lazy as _

from .views import users_activity_logs

@hooks.register('register_admin_urls')
def register_user_activity_url():
    return [
        path('users_activity_logs/', users_activity_logs, name='users_activity'),
    ]

@hooks.register('register_admin_menu_item')
def register_user_activity_menu_item():
    # Creamos un wrapper para verificar si el usuario es superusuario
    class SuperuserMenuItem(MenuItem):
        def is_shown(self, request):
            return request.user.is_superuser

    return SuperuserMenuItem(
        _('Logs de usuarios'), 
        reverse('users_activity'), 
        icon_name='user'
    )
