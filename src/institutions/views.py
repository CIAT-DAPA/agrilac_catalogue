from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django import forms
from .models import InstitutionPage
from django.core.paginator import Paginator

class AddPartnerForm(forms.Form):
    partner_email = forms.EmailField(label="Correo del socio")

def manage_partners(request, institution_id):
    institution = get_object_or_404(InstitutionPage, id=institution_id)
    
    if request.method == 'POST':
        form = AddPartnerForm(request.POST)
        if form.is_valid():
            # Busca al socio por correo
            try:
                user = get_user_model().objects.get(email=form.cleaned_data['partner_email'])
                institution.partners.add(user)
                messages.success(request, f"Socio {user.email} agregado con éxito.")
            except get_user_model().DoesNotExist:
                messages.error(request, "No se encontró un usuario con ese correo.")
        return redirect('manage_partners', institution_id=institution.id)
    
    form = AddPartnerForm()

    # Socios actuales
    current_partners = institution.partners.all()

    return render(request, 'manage_partners.html', {
        'institution': institution,
        'form': form,
        'current_partners': current_partners,
    })

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
