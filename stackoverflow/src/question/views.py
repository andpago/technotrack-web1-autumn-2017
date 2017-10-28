from django import forms
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, FormView

from answer.views import AnswerCreateForm
from .models import Question


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'question/question.html'

    def get_context_data(self, **kwargs):
        answer_form = AnswerCreateForm(initial={'question': self.get_object()})

        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        context['answer_form'] = answer_form

        return context


class QuestionListView(ListView):
    model = Question
    template_name = 'question/question_list.html'


class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text']


class QuestionCreateView(CreateView):
    template_name = 'question/question_create.html'
    form_class = QuestionCreateForm

    def form_valid(self, form):
        question = form.save(commit=False)
        question.author = self.request.user

        question.save()

        
        return super(QuestionCreateView, self).form_valid(form)
