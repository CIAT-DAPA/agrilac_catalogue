# activity_logs/utils.py
from .models import UserActivityLog
from django.utils.timezone import now

def log_user_activity(user, action, request=None, extra_data=None):
    log = UserActivityLog(
        user=user,
        action=action,
        timestamp=now(),
        extra_data=extra_data or {}
    )
    
    if request:
        log.ip_address = request.META.get('REMOTE_ADDR')
        log.user_agent = request.META.get('HTTP_USER_AGENT')
    
    log.save()
    print(log)
