# institutions/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import InstitutionPage, InstitutionMembership
from .forms import AddPartnerForm


@login_required
def institution_partners(request):
    # Obtener la institución del usuario que es dueño
    institution = get_object_or_404(InstitutionPage, owner_user=request.user)
    partners = institution.membership_set.select_related('user')
    print(partners)

    # Procesamos el formulario de adición de socio
    if request.method == 'POST':
        form = AddPartnerForm(request.POST, institution=institution)
        if form.is_valid():
            form.save()
            return redirect('partners')  # Redirigimos de vuelta a la lista de socios
    else:
        form = AddPartnerForm(institution=institution)

    return render(request, 'institutions/institution_partners.html', {
        'institution': institution,
        'partners': partners,  # Pasamos los socios al contexto
        'form': form  # Pasamos el formulario al contexto
    })


@login_required
def remove_partner(request, institution_id, partner_id):
    # Verifica que el usuario sea el dueño de la institución
    institution = get_object_or_404(InstitutionPage, id=institution_id, owner_user=request.user)

    # Buscar la relación entre la institución y el socio
    membership = get_object_or_404(InstitutionMembership, institution=institution, user_id=partner_id)
    
    if request.method == 'POST':
        # Si se confirma la eliminación, eliminar la relación (membership)
        membership.delete()
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
