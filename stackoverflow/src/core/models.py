from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.utils import timezone
from autoslug import AutoSlugField


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True, null=False, editable=False, blank=False)
    bio = models.TextField(blank=True, default='')
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()
    slug = AutoSlugField(populate_from='username')

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(type(self), self).save(*args, **kwargs)