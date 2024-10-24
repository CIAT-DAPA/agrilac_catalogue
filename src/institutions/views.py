# institutions/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from users.models import CustomUser
from .models import InstitutionPage, InstitutionMembership
from .forms import AddPartnerForm
from django.contrib import messages


@login_required
def institution_partners(request):
    # Obtener la institución del usuario que es dueño
    institution = get_object_or_404(InstitutionPage, owner_user=request.user)
    partners = institution.membership_set.select_related('user')

    # Procesamos el formulario de adición de socios con checkboxes
    if request.method == 'POST':
        selected_user_ids = request.POST.getlist('selected_users')  # Obtener IDs de los usuarios seleccionados
        if selected_user_ids:
            for user_id in selected_user_ids:
                user = CustomUser.objects.get(id=user_id)
                # Crear la relación de socio si no existe
                InstitutionMembership.objects.get_or_create(
                    user=user, 
                    institution=institution, 
                    defaults={'role': 'partner'}
                )
                # Asegurarse de que el rol del usuario se actualice a 'partner'
                if user.role != 'partner':
                    user.role = 'partner'
                    user.save()

            messages.success(request, "Socios agregados exitosamente.")
        else:
            messages.error(request, "No se seleccionaron usuarios.")
        return redirect('partners')  # Redirigimos de vuelta a la lista de socios

    # Si es una solicitud GET, mostramos el formulario y los socios actuales
    return render(request, 'institutions/institution_partners.html', {
        'institution': institution,
        'partners': partners,  # Pasamos los socios al contexto
    })

@login_required
def remove_partner(request, institution_id, partner_id):
    # Verifica que el usuario sea el dueño de la institución
    institution = get_object_or_404(InstitutionPage, id=institution_id, owner_user=request.user)

    # Buscar la relación entre la institución y el socio
    membership = get_object_or_404(InstitutionMembership, institution=institution, user_id=partner_id)
    user = membership.user 
    
    if request.method == 'POST':
        # Si se confirma la eliminación, eliminar la relación (membership)
        membership.delete()

        # Verificar si el usuario pertenece a alguna otra institución
        if not InstitutionMembership.objects.filter(user=user).exists():
            # Si no pertenece a ninguna otra institución, cambiamos su rol a 'visitor'
            user.role = CustomUser.VISITOR
            user.save()

        return redirect('partners')
    
    # Si se accede por GET, redirigir a la página de detalles de la institución
    return render(request, 'institutions/confirm_delete_partner.html', {'membership': membership})



def institution_detail(request, pk):
    institution = get_object_or_404(InstitutionPage, pk=pk)
    
    return render(request, 'institutions/institution_page.html', {'page': institution})


def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        datasets = self.datasets.all()

        # Paginador - Mostramos 5 datasets por página
        paginator = Paginator(datasets, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Estadísticas adicionales sobre datasets
        total_datasets = datasets.count()
        public_datasets = datasets.filter(type_dataset='public').count()
        restricted_datasets = datasets.filter(type_dataset='restricted').count()

        context['total_datasets'] = total_datasets
        context['public_datasets'] = public_datasets
        context['restricted_datasets'] = restricted_datasets
        context['page_obj'] = page_obj

        return context

def institution_list(request):
    instituciones = InstitutionPage.objects.live()

    return render(request, 'institutions/institution_list.html', {
        'title': 'Instituciones',
        'instituciones': instituciones,
    })
