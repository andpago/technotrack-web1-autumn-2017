from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, CreateView, FormView, UpdateView

from answer.views import AnswerCreateForm

from core.views import has_search_form, author_only_methods
from .models import Question


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'question/question.html'

    def get_context_data(self, **kwargs):
        answer_form = AnswerCreateForm(initial={'question': self.get_object()})

        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        context['answer_form'] = answer_form

        return context


@has_search_form(sort_choices=[
            ('title', 'title asc'),
            ('-title', 'title desc'),
            ('text', 'text asc'),
            ('-text', 'text desc'),
            ('author', 'author'),
            ('-author', 'author desc'),
            ('category', 'category asc'),
            ('-category', 'category desc')
])
class QuestionListView(ListView):
    model = Question
    template_name = 'question/question_list.html'


class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'category']


@method_decorator(login_required, name='dispatch')
class QuestionCreateView(CreateView):
    template_name = 'question/question_create.html'
    form_class = QuestionCreateForm

    def form_valid(self, form):
        question = form.save(commit=False)
        question.author = self.request.user
        question.save()

        return super(QuestionCreateView, self).form_valid(form)


@author_only_methods('get', 'post')
@method_decorator(login_required, name='dispatch')
class QuestionEditView(UpdateView):
    template_name = 'question/question_edit.html'
    model = Question
    fields = ['title', 'text', 'category']