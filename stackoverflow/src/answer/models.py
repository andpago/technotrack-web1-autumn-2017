from django.db import models

# Create your models here.
from django.utils import timezone
from django.conf import settings
from question.models import Question

User = settings.AUTH_USER_MODEL


class Answer(models.Model):
    author = models.ForeignKey(User)
    text = models.TextField()
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()
    question = models.ForeignKey(Question, null=False, related_name='answers')

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(type(self), self).save(*args, **kwargs)

    def __str__(self):
        return 'Answer #{} by @{}: "{}"'.format(self.pk, self.author.username, self.text[:20])

    class Meta:
        verbose_name = "answer"
        verbose_name_plural = "answers"