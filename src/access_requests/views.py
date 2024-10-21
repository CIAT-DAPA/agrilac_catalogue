# access_requests/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import AccessRequest
from datasets.models import DatasetPage
from .forms import AccessRequestForm
from django.contrib import messages
from notifications.emails import send_access_request_email

# Vista para que el usuario solicite acceso
@login_required
def request_access(request, dataset_id):
    dataset = get_object_or_404(DatasetPage, pk=dataset_id, type_dataset='restricted')
    
    if request.method == 'POST':
        form = AccessRequestForm(request.POST)
        if form.is_valid():
            access_request = form.save(commit=False)
            access_request.user = request.user
            access_request.dataset = dataset
            access_request.save()
            return redirect('user_access_requests')
    else:
        form = AccessRequestForm()

    return render(request, 'access_requests/request_access.html', {
        'dataset': dataset,
        'form': form,
    })

# Vista para que los socios/dueños revisen las solicitudes
@login_required
def review_requests(request):
    user_institutions = request.user.institution_memberships.all()
    requests = AccessRequest.objects.filter(dataset__institution_related__in=user_institutions, status='pending')
    return render(request, 'access_requests/review_requests.html', {
        'requests': requests,
    })

# Vista para que el usuario revise sus solicitudes
@login_required
def user_access_requests(request):
    requests = request.user.access_requests.all()
    return render(request, 'access_requests/user_requests.html', {
        'requests': requests,
    })

# Aprobar o rechazar solicitud

@login_required
def process_request(request, request_id, action):
    access_request = get_object_or_404(AccessRequest, pk=request_id, status='pending')
    
    if request.method == 'POST':
        access_response = request.POST.get('access_response', '')

        if action == 'approve':
            access_request.status = 'approved'
        elif action == 'deny':
            access_request.status = 'denied'
        
        access_request.access_response = access_response
        access_request.save()

        # Enviar correo al usuario solicitante
        send_access_request_email(
            access_request.user.email,
            access_request.dataset.title,
            access_request.access_response,
            access_request.status
        )
    
    return redirect('review_requests')

# Borrar una solicitud
@login_required
def delete_request(request, request_id):
    access_request = get_object_or_404(AccessRequest, pk=request_id, status='pending')

    # Asegurarse de que solo el usuario que creó la solicitud pueda eliminarla
    if access_request.user != request.user:
        messages.error(request, "No tienes permiso para eliminar esta solicitud.")
        return redirect('user_access_requests')

    if request.method == 'POST':
        access_request.delete()
        messages.success(request, "Solicitud eliminada exitosamente.")
        return redirect('user_access_requests')
    
    # Redireccionar si no es una solicitud POST
    messages.error(request, "Método no permitido.")
    return redirect('user_access_requests')
