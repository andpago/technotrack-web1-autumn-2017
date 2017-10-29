from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from answer.models import Answer
from question.models import Question

User = get_user_model()


class QuestionLike(models.Model):
    author = models.ForeignKey(User, related_name='question_likes')
    question = models.ForeignKey(Question, related_name='likes')


class AnswerLike(models.Model):
    author = models.ForeignKey(User, related_name='answer_likes')
    answer = models.ForeignKey(Answer, related_name='likes')