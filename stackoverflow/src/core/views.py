# Create your views here.
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView

from answer.models import Answer
from question.models import Question
from .models import User


class UserDetailView(DetailView):
    model = User
    template_name = 'core/user.html'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user = self.get_object()

        context['user_questions'] = user.questions.all()[:5]
        context['user_answers'] = user.answers.all()[:5]

        return context


class HomeView(View):
    def get(self, request, **kwargs):
        if 'context' in kwargs:
            context = kwargs['context']
        else:
            context = {}

        context['questions'] = Question.objects.all()[:5]
        context['answers'] = Answer.objects.all()[:5]

        kwargs['context'] = context

        return render(request, 'core/home.html', **kwargs)