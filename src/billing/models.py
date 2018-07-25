from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

from accounts.models import GuestEmail


User = settings.AUTH_USER_MODEL

# Create your models here.

class BillingProfileManager(models.Manager):
    def new_or_get_billing(self, request):
        guest_email_id = request.session.get('guest_email_id')
        user = request.user
        obj_created = False
        obj = None

        if user.is_authenticated():
            # Logged in user checkout; remember payment/billing stuff
            obj, obj_created = self.model.objects.get_or_create(
                                user=user, email=user.email)
        elif guest_email_id is not None:
            # Guest user checkout; auto reloads payment/billing stuff
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, obj_created = self.model.objects.get_or_create(
                                email=guest_email_obj.email)
        else:
            pass
        return obj, obj_created

class BillingProfile(models.Model):
    # In order to allow any user registered / guest we set null and blank parameters
    # user = models.ForeignKey(User, unique=True, null=True, blank=True)
    user = models.OneToOneField(User, null=True, blank=True)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    # Stripe or Braintree costumer id

    objects = BillingProfileManager()

    def __str__(self):
        return self.email


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(user_created_receiver, sender=User)
