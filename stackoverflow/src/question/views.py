from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView

from .models import Question


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'question/question.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        question = self.get_object()

        context['text'] = question.text
        context['author_username'] = question.author.username
        context['title'] = question.title

        return context
