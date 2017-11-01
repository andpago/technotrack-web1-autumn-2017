from django.contrib import admin
from django.db import models

# Register your models here.
from martor.widgets import AdminMartorWidget

from .models import Question, Answer


class QuestionAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget}
    }

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)