from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Colis, Transaction, CodePromo
from .resources import ColisResource
from import_export import resources
from import_export.admin import ImportExportModelAdmin


@admin.register(Colis)
class ColisAdmin(ImportExportModelAdmin):
    resource_class = ColisResource
    list_display = ('id', 'nombre_utilisations', 'etat', 'status_retour', 'date_derniere_utilisation', 'qr_code', 'utilisateur')
    list_filter = ('etat', 'status_retour', 'date_derniere_utilisation')
    search_fields = ('id', 'utilisateur__username')
    readonly_fields = ('qr_code',)
    actions = ['marquer_comme_retourne', 'marquer_comme_valide']

    def marquer_comme_retourne(self, request, queryset):
        queryset.update(status_retour='en_attente')
        self.message_user(request, "Les colis sélectionnés ont été marqués comme 'En attente de validation'.")

    marquer_comme_retourne.short_description = "Marquer comme 'En attente de validation'"

    def marquer_comme_valide(self, request, queryset):
        for colis in queryset:
            colis.valider_colis()  # Appelle la méthode valider_colis
        self.message_user(request, "Les colis sélectionnés ont été validés.")

    marquer_comme_valide.short_description = "Valider les colis"


@admin.register(Transaction)
class TransactionAdmin(ImportExportModelAdmin):  # Permet aussi l'import/export
    list_display = ('utilisateur', 'colis', 'type_action', 'date_action')
    list_filter = ('type_action', 'date_action')
    search_fields = ('utilisateur__username', 'colis__id')


@admin.register(CodePromo)
class CodePromoAdmin(ImportExportModelAdmin):  # Permet aussi l'import/export
    list_display = ('code', 'utilisateur', 'date_expiration', 'est_utilise')
    list_filter = ('est_utilise', 'date_expiration')
    search_fields = ('code', 'utilisateur__username')
