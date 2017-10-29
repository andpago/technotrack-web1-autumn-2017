from django.contrib.auth.decorators import login_required
from django.db.models import Model
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse

from answer.models import Answer
from .models import QuestionLike, AnswerLike


# Create your views here.


@login_required
def like_question(request, *args, **kwargs):
    if request.method != "POST":
        return HttpResponseBadRequest('<h1>Method ' + request.method + ' is unsupported</h1>')
    else:
        user = request.user
        question_id = request.POST.get('question_id', None)

        if question_id is None:
            return HttpResponseBadRequest('<h1>Bad request: no question specified</h1>')

        try:
            old_like = QuestionLike.objects.get(author=user, question_id=question_id)
            old_like.delete()
        except QuestionLike.DoesNotExist:
            like = QuestionLike(author=user, question_id=question_id)
            like.save()
        except QuestionLike.MultipleObjectsReturned:
            # this is very bad :(
            for like in QuestionLike.objects.filter(author=user, question_id=question_id).all():
                like.delete()

        return redirect(reverse('question:question', kwargs={'pk': question_id}))


@login_required
def like_answer(request, *args, **kwargs):
    if request.method != "POST":
        return HttpResponseBadRequest('<h1>Method ' + request.method + ' is unsupported</h1>')
    else:
        user = request.user
        answer_id = request.POST.get('answer_id', None)

        if answer_id is None:
            return HttpResponseBadRequest('<h1>Bad request: no answer specified</h1>')

        try:
            old_like = AnswerLike.objects.get(author=user, answer_id=answer_id)
            old_like.delete()
        except AnswerLike.DoesNotExist:
            like = AnswerLike(author=user, answer_id=answer_id)
            like.save()
        except AnswerLike.MultipleObjectsReturned:
            # this is very bad :(
            for like in AnswerLike.objects.filter(author=user, answer_id=answer_id).all():
                like.delete()

        question_id = Answer.objects.get(id=answer_id).question_id

        return redirect(reverse('question:question', kwargs={'pk': question_id}))