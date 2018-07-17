import random
import os

from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from ecommerce.utils import unique_slug_generator 

# Separating file basename from ext
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


# Creating a robust file path with random number as name
def upload_image_path(instance, filepath):
    print(instance)
    print(filepath)
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filepath)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return 'products/{new_filename}/{final_filename}'.format(
        new_filename=new_filename, 
        final_filename=final_filename
        )


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)
    
    def featured(self):
        return self.filter(featured=True, active=True)

    def search(self, query):
        lookups = (
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(price__icontains=query) |
            Q(tag__title__icontains=query)
        )
        return self.filter(lookups).distinct()
    

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)
    
    def all(self):
        return self.get_queryset().active()

    def features(self):
        # return self.get_queryset().filter(featured=True)
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id) # Product.objects == self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)


# Create your models here.
class Product(models.Model):
    title        = models.CharField(max_length=120)
    slug         = models.SlugField(blank=True, unique=True)
    description  = models.TextField()
    price        = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    # image        = models.FileField(upload_to=upload_image_path, null=True, blank=True)
    image        = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured     = models.BooleanField(default=False)
    active       = models.BooleanField(default=True)
    timestamp    = models.DateTimeField(auto_now_add=True)
    # Overriding the objects manager with our manager
    objects = ProductManager()

    def get_absolute_url(self):
        # return "/products/{slug}/".format(slug=self.slug)
        # Now using reverse to avoid conflicts in path changing
        # Inside reverse <urlnamespace>:<urlname>
        return reverse('products:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    # Python2 version
    def __unicode__(self):
        return self.title


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)