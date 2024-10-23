# activity_logs/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import UserActivityLog

@login_required
def users_activity_logs(request):
    if not request.user.is_superuser:
        return render(request, '403.html')  # O la plantilla que uses para errores 403

    logs = UserActivityLog.objects.all().order_by('-timestamp')
    print(logs)
    return render(request, 'activity_logs/user_logs.html', {'logs': logs})
