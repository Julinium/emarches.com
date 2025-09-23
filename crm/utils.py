from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth import get_user_model

def get_user_sessions(user):
    """
    Retrieve all active sessions for a given user.
    """
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_sessions = []

    for session in active_sessions:
        session_data = session.get_decoded()
        user_id = session_data.get('_auth_user_id')
        if user_id and str(user_id) == str(user.id):
            user_sessions.append({
                'user_id': user_id,
                'session_key': session.session_key,
                'expire_date': session.expire_date,
                'last_activity': session_data.get('last_activity', None),
            })

    return user_sessions