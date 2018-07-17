from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL

# Create your models here.

class BillingProfile(models.Model):
    # In order to allow any user registered / guest we set null and blank parameters
    user = models.ForeignKey(User, unique=True, null=True, blank=True)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    # Stripe or Braintree costumer id

    def __str__(self):
        return self.email


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created:
        BillingProfile.objects.get_or_create(user=instance)

post_save.connect(user_created_receiver, sender=User)
