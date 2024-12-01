import qrcode
import uuid
from io import BytesIO
from django.db import models
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    from .models import Profil  # Import évite une boucle circulaire
    if created:
        # Créer un profil pour chaque nouvel utilisateur
        Profil.objects.create(utilisateur=instance)
    else:
        # S'assurer que chaque utilisateur a un profil
        if not hasattr(instance, 'profil'):
            Profil.objects.create(utilisateur=instance)

def generate_short_id():
    return str(uuid.uuid4())[:10]


class Profil(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)  # Score de l'utilisateur

    def __str__(self):
        return f"{self.utilisateur.username} - Score: {self.score}"


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profil.save()


class Colis(models.Model):
    STATUS_CHOICES = [
        ('en_attente', 'En attente de validation'),
        ('validé', 'Validé'),
        ('aucun', 'Aucun'),
    ]

    id = models.CharField(max_length=100, primary_key=True)
    nombre_utilisations = models.IntegerField(default=0)
    etat = models.CharField(max_length=100, default='nouveau')
    date_derniere_utilisation = models.DateTimeField(null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status_retour = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aucun')

    def generate_qr_code(self):
        """
        Génère un QR code basé sur l'ID du colis et sauvegarde dans le champ `qr_code`.
        """
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(f"http://127.0.0.1:8000/colis/{self.id}/")
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        self.qr_code.save(f"{self.id}.png", ContentFile(buffer.read()), save=False)
        buffer.close()

    def calcul_economie_co2(self):
        economie_co2 = (0.56 * self.nombre_utilisations) - 4.6
        if self.nombre_utilisations >= 9:
            return f"🌱 Bravo ! Ton colis a déjà permis d’économiser {economie_co2:.2f} kg de CO2 🎉"
        
        return None
    
    def valider_colis(self):
        """
        Valide le colis et met à jour les informations associées.
        """
        if self.utilisateur:  # Vérifie qu'un utilisateur est lié
            # Incrémente le score de l'utilisateur
            profil = Profil.objects.get(utilisateur=self.utilisateur)
            profil.score += 100
            profil.save()

            # Incrémente le nombre d'utilisations
            self.nombre_utilisations += 1

            # Réinitialise les champs utilisateur et status_retour
            self.utilisateur = None
            self.status_retour = "aucun"

            # Sauvegarde les modifications
            self.save()


    def __str__(self):
        return f"Colis {self.id} (Statut: {self.status_retour})"


class Transaction(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    colis = models.ForeignKey(Colis, on_delete=models.CASCADE)
    type_action = models.CharField(
        max_length=50,
        choices=[
            ('retour', 'Retour'),
            ('reutilisation', 'Réutilisation'),
            ('retour_vendeur', 'Retour au vendeur'),
        ],
    )
    date_action = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        utilisateur_nom = self.utilisateur.username if self.utilisateur else "Utilisateur inconnu"
        return f"{self.type_action} par {utilisateur_nom} le {self.date_action}"


class CodePromo(models.Model):
    code = models.CharField(max_length=20, unique=True)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    date_expiration = models.DateField()
    est_utilise = models.BooleanField(default=False)

    def __str__(self):
        return f"Code {self.code} pour {self.utilisateur.username}"
