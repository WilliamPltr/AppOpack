import random
import uuid
from django.core.management.base import BaseCommand
from core.models import Colis

class Command(BaseCommand):
    help = "Génère 50 colis avec des valeurs aléatoires"

    def handle(self, *args, **kwargs):
        etats = ['chez_client', 'en_transit', 'retourne', 'stationnement']
        colis_crees = []

        for _ in range(50):
            colis = Colis(
                id=str(uuid.uuid4())[:10],  # Génère un ID unique de 10 caractères
                nombre_utilisations=random.randint(0, 100),  # Génère un nombre entre 0 et 100
                etat=random.choice(etats),  # Choisit un état au hasard
            )
            colis.generate_qr_code()  # Génère un QR code
            colis_crees.append(colis)

        # Sauvegarde les colis en une seule fois pour optimiser les performances
        Colis.objects.bulk_create(colis_crees)

        self.stdout.write(self.style.SUCCESS(f"50 colis ont été créés avec succès !"))
