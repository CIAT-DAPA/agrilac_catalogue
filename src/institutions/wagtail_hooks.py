
from django.core.exceptions import PermissionDenied
from wagtail import hooks
from .models import InstitutionPage

class InstitutionPagePermissionHelper:
    def user_can_edit_obj(self, user, page):
        # Verifica si el usuario es el dueño de la institución o un socio
        if hasattr(page.specific, 'institution_memberships'):
            if user == page.specific.owner_user:
                return True
            if user.institution_memberships.filter(pk=page.pk).exists():
                return True
        # Si no es dueño ni socio, no tiene permiso
        return False
    
# @hooks.register('construct_page_permission_checker')
# def construct_page_permission_checker(page, request):
#     if isinstance(page, InstitutionPage):
#         # Solo permitir la edición si el usuario es el dueño o socio
#         return InstitutionPagePermissionHelper(page, request.user)
    
@hooks.register('before_edit_page')
def restrict_institution_editing(request, page):
    permission_helper = InstitutionPagePermissionHelper()
    # Verifica si la página es una InstitutionPage y si el usuario tiene permiso
    if isinstance(page.specific, InstitutionPage):
        if not permission_helper.user_can_edit_obj(request.user, page):
            raise PermissionDenied  # Bloquea la edición si no tiene permiso