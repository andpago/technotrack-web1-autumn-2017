from django.contrib import admin

# Register your models here.
from .models import QuestionCategory

admin.site.register(QuestionCategory)