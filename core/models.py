from django.db import models

# Create your models here.


class ModuleRegistry(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    is_installed = models.BooleanField(default=False)
    version = models.CharField(max_length=20, default='1.0.0')
    landing_url = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name
