from wagtail import hooks
from django.templatetags.static import static
from django.core.exceptions import PermissionDenied
from wagtail import hooks
from .models import DatasetPage

class DatasetPagePermissionHelper:
    def user_can_edit_obj(self, user, page):
        # Verifica si el dataset está relacionado con una institución
        if hasattr(page.specific, 'institution_related') and page.specific.institution_related:
            institution = page.specific.institution_related
            # Permitir que los superusuarios puedan editar cualquier página
            if user.is_superuser:
                return True
            # Verifica si el usuario es el dueño de la institución o socio
            if user == institution.owner_user:
                return True
            if user.institution_memberships.filter(pk=institution.pk).exists():
                return True
        # Si no es dueño ni socio, no tiene permiso
        return False

@hooks.register('before_edit_page')
def restrict_dataset_editing(request, page):
    permission_helper = DatasetPagePermissionHelper()
    # Verifica si la página es un DatasetPage y si el usuario tiene permiso
    if isinstance(page.specific, DatasetPage):
        if not permission_helper.user_can_edit_obj(request.user, page):
            raise PermissionDenied  # Bloquea la edición si no tiene permiso