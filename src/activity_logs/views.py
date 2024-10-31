from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from .models import UserActivityLog

@login_required
def users_activity_logs(request):
    # Asegúrate de que solo los usuarios superadministradores puedan acceder
    if not request.user.is_superuser:
        return render(request, '403.html')  # O la plantilla que uses para errores 403

    # Obtén el término de búsqueda de los parámetros GET
    query = request.GET.get('q', '').strip()
    logs = UserActivityLog.objects.all().order_by('-timestamp')

    # Si hay una consulta de búsqueda, filtra los logs
    if query:
        logs = logs.filter(
            user__username__icontains=query
        ) | logs.filter(
            action__icontains=query
        )
    
    # Agrupa los logs por usuario para mostrarlos en la plantilla
    grouped_logs = defaultdict(list)
    for log in logs:
        grouped_logs[log.user].append(log)
    
    grouped_logs = dict(grouped_logs)
    return render(request, 'activity_logs/user_logs.html', {
        'grouped_logs': grouped_logs,
        'query': query  # Pasa el término de búsqueda a la plantilla para que se muestre en el campo
    })
