def get_next_url(request):
    """
    Vérifie si `next` est déjà dans les GET ou POST. Sinon, utilise `HTTP_REFERER` pour mémoriser.
    """
    next_url = request.GET.get('next') or request.POST.get('next')
    if not next_url:
        next_url = request.META.get('HTTP_REFERER', '/')  # Utilise la page précédente comme fallback
    return next_url

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class EmailBackend(BaseBackend):
    """
    Custom authentication backend using email and password.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email=username)  # Use email to authenticate
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def authenticate_by_email(email, password):
    """
    Wrapper function to authenticate using the EmailBackend.
    """
    backend = EmailBackend()
    user = backend.authenticate(request=None, username=email, password=password)
    return user, 'core.utils.EmailBackend' if user else (None, None)