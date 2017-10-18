from django.db import models

# Create your models here.
from django.utils import timezone


class BaseCategory(models.Model):
    name = models.CharField(max_length=255)

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    class Meta:
        abstract = True

    def __str__(self):
        return "<{}: name={}>".format(type(self).__name__, self.name)

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(BaseCategory, self).save(*args, **kwargs)


class QuestionCategory(BaseCategory):
    class Meta:
        verbose_name = "question category"
        verbose_name_plural = "question categories"
