from django.contrib.auth import get_user_model
from question.models import Question
from answer.models import Answer
from category.models import QuestionCategory
from django.template import Library

register = Library()
User = get_user_model()


@register.simple_tag
def count_objects(cls):
    cls = {c.__name__: c for c in [Question, Answer, QuestionCategory, User]}.get(cls, None)
    return cls.objects.count() if cls is not None else ""
