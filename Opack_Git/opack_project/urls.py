from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core import views
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from core.views import CustomLoginView
from django.contrib.auth import views as auth_views
from core.views import (
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView
)
from django.http import HttpResponse

# Example view for the root path
def root_view(request):
    return HttpResponse("Welcome to the Opack application!")
    
urlpatterns = [
    # Administration
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),

    # Authentification
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    # Gestion des colis
    path('colis/<slug:colis_id>/', views.scan_colis, name='scan_colis'),
    path('colis/<slug:colis_id>/retour/', views.retour_colis, name='retour_colis'),
    path('colis/<slug:colis_id>/reutiliser/', views.reutiliser_colis, name='reutiliser_colis'),
    path('colis/<slug:colis_id>/retour_vendeur/', views.retourner_vendeur, name='retourner_vendeur'),

    # Compte utilisateur
    path('account/', views.account_view, name='account'),
    path('accueil/', views.accueil, name='accueil'),

    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('', root_view),  # Define root URL
]

# Ajout des fichiers médias en mode DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
