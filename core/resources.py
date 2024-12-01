from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Colis
from django.conf import settings

class ColisResource(resources.ModelResource):
    utilisateur = fields.Field(column_name='Utilisateur', attribute='utilisateur', widget=ForeignKeyWidget(model='auth.User', field='username'))
    qr_code_url = fields.Field(column_name='Qr code')

    class Meta:
        model = Colis
        skip_unchanged = True
        report_skipped = True
        fields = ('id', 'nombre_utilisations', 'etat', 'status_retour', 'date_derniere_utilisation', "qr_code_url", 'utilisateur')
        export_order = fields

    def dehydrate_utilisateur(self, obj):
        """Retourne le nom de l'utilisateur ou une chaîne vide."""
        return obj.utilisateur.username if obj.utilisateur else ""

    def dehydrate_qr_code_url(self, obj):
        """Retourne l'URL complète pour le QR code."""
        if obj.qr_code:
            # Assure que l'URL complète est retournée
            return f"{settings.SITE_URL}{obj.qr_code.url}"
        return ""
