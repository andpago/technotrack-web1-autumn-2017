from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

# Create your models here.


class Question(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=255, null=False)
    text = models.TextField()
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(type(self), self).save(*args, **kwargs)