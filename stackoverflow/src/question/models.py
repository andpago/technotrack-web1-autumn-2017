from django.db import models
from django.conf import settings
from django.utils import timezone

from category.models import QuestionCategory

User = settings.AUTH_USER_MODEL

# Create your models here.


class Question(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=255, null=False)
    text = models.TextField()
    category = models.ForeignKey(QuestionCategory, related_name='questions', null=True)

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(type(self), self).save(*args, **kwargs)

    def __str__(self):
        return 'Question #{} by @{}: "{}"'.format(self.pk, self.author.username, self.title[:20])

    class Meta:
        verbose_name = "question"
        verbose_name_plural = "questions"